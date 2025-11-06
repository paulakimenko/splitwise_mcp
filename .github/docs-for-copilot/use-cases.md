# Use Case Examples

**For technical implementation details and API patterns to accomplish these use cases, refer to the main developer documentation:**

📋 **[Splitwise MCP Service - Developer Instructions](../copilot-instructions.md)**

This document contains:
- Architecture overview and component descriptions
- MCP tool patterns and implementation examples
- API integration patterns with the Splitwise OpenAPI specification
- Development workflows and testing procedures
- Code style standards and best practices

---

## Common Splitwise Operations

Below are comprehensive use cases demonstrating real-world expense management workflows. Each example shows how to leverage the full capabilities of the Splitwise API through MCP tools, REST endpoints, and custom helpers.

### 🏠 **Group & Friendship Management**

#### **1. Create a New Household Group**
```
Create group "Downtown Apartment 2025" with type "home" and simplify_by_default=true. 
Add members: alice@example.com, bob@example.com, and charlie@example.com.
```
*Uses: `create_group` with user email invitations and automatic friend creation*

#### **2. Manage Trip Planning Group**
```
Create group "Tokyo Adventure 2025" with type "trip". 
Add existing friends: Sarah (ID: 12345) and new member mike@travels.com.
Generate invite link for additional participants.
```
*Uses: `create_group`, `add_user_to_group` with mixed user types*

#### **3. Friend Network Expansion**
```
Add multiple friends in batch: 
- Emma Thompson (emma.t@company.com)
- James Wilson (j.wilson@university.edu) 
- Lisa Chen (existing user ID: 67890)
```
*Uses: `create_friends` with mixed identification methods*

### 💰 **Expense Creation & Management**

#### **4. Restaurant Bill with Unequal Shares**
```
Add expense "Fancy Dinner at Le Bernardin" for $280.00 USD to group "Friends NYC":
- Alice paid $280.00, owes $70.00 (25%)
- Bob paid $0.00, owes $84.00 (30%) 
- Carol paid $0.00, owes $56.00 (20%)
- David paid $0.00, owes $70.00 (25%)
Category: "Dining out", Date: 2025-11-05, Notes: "Birthday celebration"
```
*Uses: `create_expense` with custom shares and category assignment*

#### **5. Recurring Monthly Utilities**
```
Add recurring expense "Internet & Cable" for $120.00 USD to "Apartment Group":
- Split equally among 3 roommates
- Repeat: monthly, Email reminder: 3 days before
- Category: "Internet", Auto-pay by current user
```
*Uses: `create_expense` with repeat_interval and email_reminder settings*

#### **6. Travel Expense with Receipt**
```
Add expense "Flight to Barcelona" for €450.00 EUR:
- Upload receipt image, Category: "Airplane"
- Split equally with travel companion Sarah
- Date: 2025-12-15 (future trip)
```
*Uses: `create_expense` with receipt attachment and international currency*

### 📊 **Reporting & Analytics**

#### **7. Monthly Category Breakdown**
```
Generate detailed report for "House Expenses" group for October 2025:
- Show spending by category (Groceries, Utilities, Rent, etc.)
- Calculate each member's contribution vs. consumption
- Identify top 3 expense categories and spending trends
- Provide recommendations for November budget
```
*Uses: `list_expenses` with date filters, custom analytics processing*

#### **8. Cross-Group Financial Summary**
```
Analyze user's financial position across all groups:
- Outstanding balances in "Apartment", "Friends", "Travel" groups  
- Total owed TO user vs. owed BY user
- Currency conversion to USD for unified view
- Generate payment priorities and settlement suggestions
```
*Uses: `list_groups`, `get_friend` balances, multi-currency processing*

#### **9. Expense Trend Analysis**
```
Compare spending patterns: Q3 2025 vs Q4 2025 for "Family Expenses":
- Monthly spending velocity and category shifts
- Per-person expense behavior changes  
- Seasonal spending patterns (utilities, travel, etc.)
- Budget variance analysis with visual charts
```
*Uses: `list_expenses` with date ranges, statistical analysis*

### 🔍 **Search & Filtering**

#### **10. Smart Expense Discovery**
```
Find all expenses in "Vacation Group" containing "uber", "taxi", or "transport":
- Search descriptions and comments for keywords
- Filter by date range: June 2025 - August 2025  
- Show total transportation costs per person
- Identify most frequent transport vendors
```
*Uses: `list_expenses` with keyword filtering, text analysis*

#### **11. High-Value Expense Audit**
```
Identify expenses > $200 USD in "Business Travel" group for tax reporting:
- Convert all currencies to USD using historical rates
- Filter by categories: "Meals", "Lodging", "Transportation"  
- Export to CSV with receipt URLs and tax classifications
- Flag expenses missing receipts or proper categorization
```
*Uses: `list_expenses` with amount filters, currency conversion, export formatting*

### 💳 **Payment & Settlement**

#### **12. Optimal Debt Settlement**
```
Calculate minimal payment transfers for "House Group" with 6 members:
- Current balances: Alice owes $45, Bob owes $12, Carol is owed $73, etc.
- Generate 2-3 payments to settle all debts (debt simplification)
- Consider payment preferences (Venmo, cash, bank transfer)
- Create settlement plan with payment instructions
```
*Uses: `get_group` balances, debt optimization algorithms*

#### **13. Payment Recording**
```
Record payment: "Alice paid Bob $85.50 via Venmo" for "Apartment Expenses":
- Create payment expense (not split expense)
- Update individual balances accordingly
- Add transaction reference: "Venmo: @alice-smith-123" 
- Send notification to relevant group members
```
*Uses: `create_expense` with payment=true, notification system*

### 📝 **Advanced Expense Editing**

#### **14. Retroactive Expense Modification**
```
Update expense "Grocery Shopping" (ID: 789123):
- Change amount from $87.50 to $92.75 (forgot tax)
- Add new participant: Emma (emma@email.com)  
- Redistribute shares: equal 4-way split instead of 3-way
- Add comment: "Updated with correct receipt total"
- Preserve expense history and notify affected users
```
*Uses: `update_expense` with participant changes, audit trail*

#### **15. Bulk Expense Category Assignment**
```
Update 15 uncategorized expenses from "Europe Trip 2025":
- "Restaurant Le Petit" → "Dining out"  
- "Airbnb Barcelona" → "Lodging"
- "Metro tickets" → "Public transportation"
- Batch update with smart category suggestions based on description
```
*Uses: `update_expense` in batch, category matching algorithms*

### 🌍 **Multi-Currency & International**

#### **16. International Trip Expense Management**
```
Handle expenses for "Asian Backpacking" group across 4 countries:
- Track expenses in JPY (Japan), KRW (South Korea), THB (Thailand), VND (Vietnam)
- Auto-convert to USD base currency using daily exchange rates
- Show both original and converted amounts in expense list
- Calculate fair splits accounting for currency fluctuations
```
*Uses: `create_expense` with multiple currencies, real-time conversion*

#### **17. Currency Migration Project**
```
Convert all EUR expenses in "Berlin Semester" to USD for returning students:
- Identify 50+ expenses from 6-month period  
- Apply historical exchange rates by expense date
- Update expense display currency while preserving original amounts
- Generate conversion summary report for accounting
```
*Uses: `list_expenses`, `update_expense`, historical currency APIs*

### 🔔 **Notifications & Communication**

#### **18. Expense Comment Discussions**
```
Manage expense discussion for "Team Lunch" expense:
- Alice comments: "Can we split wine separately? I didn't drink"
- Bob replies: "Good point, wine was $45 total"  
- Update expense with separate wine item
- Notify all participants of the expense modification
```
*Uses: `create_comment`, `get_comments`, `update_expense` workflow*

#### **19. Notification Management**
```
Process user's notification queue:
- 5 new expense additions in various groups
- 2 friend requests from new users
- 3 expense updates requiring attention  
- 1 group invitation pending acceptance
- Mark relevant notifications as read, prioritize action items
```
*Uses: `get_notifications`, notification filtering and processing*

### 📈 **Business & Tax Features**

#### **20. Business Expense Categorization**
```
Organize "Startup Expenses" group for tax purposes:
- Categorize by IRS business expense types
- Track receipt compliance (required for >$75 expenses)
- Generate quarterly reports by expense type
- Flag personal vs. business expenses for proper classification
```
*Uses: Custom category mapping, receipt validation, compliance reporting*

#### **21. Mileage and Per-Diem Tracking**
```
Track business travel for "Sales Team" group:
- Record mileage expenses with GPS data
- Apply standard IRS mileage rates ($0.67/mile for 2025)
- Track per-diem meal allowances by city
- Generate IRS-compliant expense reports
```
*Uses: Custom expense types, rate calculations, compliance formatting*

### 🏡 **Household & Shared Living**

#### **22. Roommate Utility Distribution**
```
Manage "4BR House" utilities with occupancy-based splitting:
- Electricity: split by room size (30%, 25%, 25%, 20%)
- Internet: equal 4-way split  
- Water: split by occupancy days (account for travel)
- Generate monthly utility summary with usage trends
```
*Uses: Custom splitting logic, occupancy tracking, utility analytics*

#### **23. Household Supply Management**
```
Track shared household purchases for "Family Home":
- Groceries: split by family size and dietary restrictions
- Cleaning supplies: equal split among adult members
- Bulk purchases: track usage and reimburse fairly
- Set up automatic recurring expenses for regular bills
```
*Uses: `create_expense` with custom allocation rules, recurring expenses*

### 🎯 **Special Scenarios**

#### **24. Event Planning & Coordination**
```
Organize "Wedding Party" expense management:
- Track deposits, vendor payments, and shared costs
- Handle guest contributions and gift tracking  
- Manage multiple currencies for international guests
- Generate final cost breakdown for wedding couple
```
*Uses: Complex group management, guest coordination, financial reporting*

#### **25. Seasonal Expense Patterns**
```
Analyze "Ski House" group for winter season planning:
- Track seasonal expenses: lift tickets, rentals, food, utilities
- Compare costs across 3 winter seasons  
- Predict upcoming season budget needs
- Optimize group composition for cost efficiency
```
*Uses: Historical analysis, predictive budgeting, seasonal optimization*

### 🔧 **Administrative & Maintenance**

#### **26. Group Archive & Restoration**
```
Archive completed "Summer Camp 2025" group:
- Export all expenses and receipts for records
- Archive group to reduce active group clutter  
- Maintain data accessibility for future reference
- Handle final balance settlements before archiving
```
*Uses: `delete_group`, data export, balance verification*

#### **27. User Profile & Preference Management**
```
Update user settings and preferences:
- Change default currency from USD to EUR
- Update notification preferences for different group types
- Modify profile information and privacy settings
- Sync preferences across multiple devices
```
*Uses: `update_user`, preference synchronization, profile management*

### 📱 **Integration & Automation**

#### **28. Smart Receipt Processing**
```
Automate expense creation from receipt photos:
- OCR processing to extract amount, date, vendor, items
- Smart category assignment based on vendor and items
- Automatic participant suggestions based on location/time
- Review and approval workflow before expense creation
```
*Uses: Receipt processing, AI categorization, workflow automation*

#### **29. Bank Integration & Reconciliation**
```
Sync with bank/credit card transactions:
- Match bank transactions to Splitwise expenses
- Identify missing expenses from transaction history
- Auto-suggest expense creation for large transactions  
- Flag discrepancies between actual and recorded expenses
```
*Uses: Financial data integration, transaction matching, discrepancy detection*

### 🌟 **Advanced Analytics**

#### **30. Spending Behavior Analysis**
```
Generate personalized spending insights:
- Compare user's spending vs. group averages
- Identify spending categories with highest variance
- Suggest budget optimizations based on patterns
- Provide recommendations for expense reduction
```
*Uses: Behavioral analytics, comparative analysis, recommendation engine*
