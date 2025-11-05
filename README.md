# Splitwise MCP Service

This repository contains a **Magic Control Panel (MCP)** server for the
Splitwise API.  The goal of this project is to expose all Splitwise
API methods through a single service while persisting the received
data into a MongoDB database, logging every request/response, and
offering REST endpoints to retrieve the cached data.  Additionally we
provide a set of higher‑level helper endpoints to handle common
scenarios expressed in Ukrainian such as adding expenses evenly or
generating monthly reports.

## Features

* ✅ **Mapping of Splitwise API methods** – each Splitwise method
  (e.g. `getGroups`, `createExpense`) is exposed as a POST route under
  `/mcp/{method_name}`.  When invoked, the server calls the underlying
  Splitwise API via the [`splitwise` Python client](https://github.com/namaggarwal/splitwise),
  stores the returned data in the database, logs the call, and
  responds with a normalised JSON representation of the result.

* ✅ **Database persistence** – results are persisted in MongoDB
  collections named after the API method (e.g. `groups`, `expenses`) along
  with a timestamp.  A separate `logs` collection captures
  metadata about each request/response pair for auditing.

* ✅ **REST endpoints** – in addition to the MCP routes the
  application provides GET endpoints such as `/groups`, `/expenses`,
  etc. which read from MongoDB and return cached data.  These
  endpoints closely mirror Splitwise’s own HTTP API but without
  triggering calls to Splitwise – useful for quick lookups or
  offline access.

* ✅ **Custom helper methods** – based on the examples below the
  server implements richer workflows such as evenly splitting an
  expense with a specific user, generating category reports for a
  month, modifying groups or expenses and optimising debt
  distribution.

* ✅ **Dockerised** – the repository includes a `Dockerfile` and
  `docker-compose.yml` to simplify deployment.  The recommended
  hosting target for production is [Hetzner](https://www.hetzner.com/) or any other
  platform capable of running Docker containers.  See
  **Deployment** below for details.

## Quick Start

1. **Clone the repository**

   ```bash
   git clone https://your-repo-url.git
   cd splitwise_mcp
   ```

2. **Install dependencies** (for local development)

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set environment variables**.  Create a `.env` file based on
   `.env.example` and provide your Splitwise personal API token and
   MongoDB connection URI (you can use a local `mongodb://localhost:27017`).

4. **Run the server**

   ```bash
   uvicorn splitwise_mcp.main:app --reload
   ```

5. **Interact via Swagger** at [`http://localhost:8000/docs`](http://localhost:8000/docs).

## Deployment

The project is designed for containerised deployment.  An example
`docker-compose.yml` is provided to spin up the FastAPI service
alongside a MongoDB instance.  On Hetzner you can either run this
compose file directly on a cloud server or build/push the Docker
image to your registry and use a managed environment such as
EasyPanel.

**Basic flow for deployment:**

1. Build and push your image:

   ```bash
   docker build -t your-dockerhub-user/splitwise-mcp:latest .
   docker push your-dockerhub-user/splitwise-mcp:latest
   ```

2. Configure your Hetzner/EasyPanel service:

   * Set the container image to `your-dockerhub-user/splitwise-mcp:latest`.
   * Add environment variables for `SPLITWISE_API_KEY`, `MONGO_URI` and
     optionally `BASE_URL` (e.g. `https://sw-mcp.paulakimenko.xyz`).
   * Expose port **8000** (FastAPI default).
   * Optionally run the provided `docker-compose.yml` if you need
     MongoDB on the same host.

3. Point your domain (`https://sw-mcp.paulakimenko.xyz`) to the
   deployed service.  Ensure HTTPS termination is handled by your
   provider or reverse proxy.

## Custom Usage Examples (Ukrainian)

The following examples demonstrate how the MCP server can fulfil
common Splitwise scenarios in Ukrainian.  Replace `GROUP_NAME`,
`USER_NAME`, etc. with real values:

| Задача | Приклад виклику |
|-------|----------------|
| Додати витрату `AMOUNT CURRENCY` у групу `GROUP_NAME` порівну з `USER_NAME` з коментарем `COMMENT` | `POST /custom/add_expense_equal_split` з тілом `{ "group_name": "Подорож", "amount": 100, "currency_code": "UAH", "participant_name": "Іван", "description": "Вечеря" }` |
| Показати витрати у групі за місяць | `GET /custom/expenses_by_month?group_name=Подорож&month=2025-10` |
| Створити групу та додати користувача | `POST /custom/create_group` з тілом `{ "name": "Квартира", "user_email": "example@example.com" }` |
| Вивести список активних груп | `GET /groups` |
| Модифікувати групу (simplify_by_default) | `PATCH /custom/update_group` з тілом `{ "group_id": 12345, "simplify_by_default": true }` |
| Змінити суму витрат на житло за місяць | `POST /custom/update_expense_amount_by_category` з тілом `{ "group_name": "Квартира", "month": "2025-10", "category": "rent", "new_amount": 3000 }` |
| Розподілити витрату частинами | `POST /custom/split_expense_custom` з тілом `{ "group_name": "Квартира", "expense_name": "Комунальні", "participant_name": "Іван", "ratio": 3 }` |
| Звіт за минулий місяць по категоріях | `GET /custom/monthly_report?group_name=Квартира&month=2025-09` |

## Contributing

Pull requests are welcome!  If you find a bug or want to add
additional helper endpoints, feel free to open an issue or submit a
patch.  Please ensure your code is formatted with `black` and that
unit tests (if any) pass.
