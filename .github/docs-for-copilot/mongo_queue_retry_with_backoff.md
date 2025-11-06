# Micro Queue Design: Scheduled Retry & Requeue (MongoDB)
## + Exponential Backoff (with jitter)

This document extends the micro-queue pattern for the **`task`** entity with **scheduled retry / requeue** and **exponential backoff**.  
Goal: prevent retry storms, smooth load, and recover “stuck” tasks safely.

---

## Data Model: `task`

```json
{
  "_id": "ObjectId",
  "payload": { /* task data */ },
  "status": "pending" | "processing" | "done" | "failed",
  "created_at": "ISODate",
  "updated_at": "ISODate",
  "attempts": 0,
  "next_retry_at": "ISODate | null",
  "backoff_policy": {
    "base_sec": 5,
    "factor": 2.0,
    "max_sec": 1800,
    "jitter": "full"
  },
  "error": { "message": "string", "code": "string", "at": "ISODate" }
}
```

> `backoff_policy` may be global or per-task.  
> `next_retry_at` allows time-delayed requeue scheduling.

---

## Task Lifecycle

| Status       | Meaning |
|--------------|---------|
| `pending`    | Task is waiting to be processed. |
| `processing` | A worker has claimed this task. |
| `done`       | Task completed successfully. |
| `failed`     | Task permanently failed (exceeded retries or irrecoverable). |

---

## Worker: Atomic Task Pop (Lock)

```python
from datetime import datetime
from pymongo import ReturnDocument

now = datetime.utcnow()
task = db.tasks.find_one_and_update(
    {
        "status": "pending",
        "$or": [{"next_retry_at": None}, {"next_retry_at": {"$lte": now}}]
    },
    {
        "$set": {"status": "processing", "updated_at": now}
    },
    sort=[("created_at", 1)],
    return_document=ReturnDocument.AFTER
)
```

---

## Mark Success

```python
def mark_done(task_id):
    db.tasks.update_one(
        {"_id": task_id},
        {"$set": {"status": "done", "updated_at": datetime.utcnow()}}
    )
```

---

## Mark Hard Failure

```python
def mark_failure(task_id, message, code=None):
    db.tasks.update_one(
        {"_id": task_id},
        {
            "$set": {
                "status": "failed",
                "updated_at": datetime.utcnow(),
                "error": {"message": message, "code": code, "at": datetime.utcnow()}
            }
        }
    )
```

---

## Exponential Backoff with Jitter

```python
import random
from datetime import datetime, timedelta

def compute_backoff_seconds(attempts, base_sec=5, factor=2.0, max_sec=1800, jitter="full"):
    raw = min(base_sec * (factor ** max(0, attempts - 1)), max_sec)

    if jitter == "none":
        return raw
    if jitter == "full":
        return random.uniform(0, raw)
    if jitter == "decorrelated":
        return min(max_sec, random.uniform(base_sec, max(base_sec, raw)))
    return raw
```

---

## Schedule Next Retry

```python
def schedule_next_retry(task):
    now = datetime.utcnow()
    policy = task.get("backoff_policy", {})
    base = policy.get("base_sec", 5)
    factor = policy.get("factor", 2.0)
    max_sec = policy.get("max_sec", 1800)
    jitter = policy.get("jitter", "full")

    attempts = int(task.get("attempts", 0)) + 1
    delay = compute_backoff_seconds(attempts, base, factor, max_sec, jitter)
    return now + timedelta(seconds=delay), attempts
```

---

## Mark Retry (Recoverable Error)

```python
def mark_retry(task):
    now = datetime.utcnow()
    next_time, attempts = schedule_next_retry(task)

    db.tasks.update_one(
        {"_id": task["_id"]},
        {
            "$set": {
                "status": "pending",
                "next_retry_at": next_time,
                "updated_at": now
            },
            "$inc": {"attempts": 1}
        }
    )
```

---

## Scheduled Requeue: Reclaim Stuck Tasks

```python
from datetime import timedelta, datetime

VISIBILITY_TIMEOUT_MIN = 10
now = datetime.utcnow()

db.tasks.update_many(
    {
        "status": "processing",
        "updated_at": {"$lt": now - timedelta(minutes=VISIBILITY_TIMEOUT_MIN)}
    },
    {
        "$set": {"status": "pending", "updated_at": now},
        "$inc": {"attempts": 1}
    }
)
```

---

## Scheduled Retry Eligibility Sweep

```python
now = datetime.utcnow()

db.tasks.update_many(
    {
        "status": "pending",
        "next_retry_at": {"$ne": None, "$lte": now}
    },
    {
        "$set": {"next_retry_at": None, "updated_at": now}
    }
)
```

---

## Max Attempts & Dead Letter Queue

```python
MAX_ATTEMPTS = 10
db.tasks.update_many(
    {"attempts": {"$gt": MAX_ATTEMPTS}, "status": {"$in": ["pending", "processing"]}},
    {"$set": {"status": "failed", "updated_at": datetime.utcnow()}}
)
```

(Optional: move to `tasks_dlq`)

---

## Recommended Indexes

```python
db.tasks.create_index([("status", 1), ("created_at", 1)])
db.tasks.create_index([("next_retry_at", 1)])
db.tasks.create_index([("status", 1), ("updated_at", 1)])
```

---

## Summary

- Prevents lost tasks via scheduled requeue.
- Avoids retry storms via exponential backoff + jitter.
- Suitable for small/medium asynchronous workloads.
- No external broker required.
