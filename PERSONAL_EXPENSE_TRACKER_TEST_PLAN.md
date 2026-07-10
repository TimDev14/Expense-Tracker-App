# Personal Expense Tracker: Functionality Test Plan

These are tests to perform while building the app. They are written as acceptance tests so they can be run manually now and converted into automated frontend/API tests once the application code exists.

## Test setup

- Use a separate test database; never run destructive tests against real data.
- Create two accounts: **User A** and **User B**.
- Create for User A an expense category named Food, an income category named Salary, two expense transactions in the selected month, one expense transaction in a prior month, and a Food budget for the selected month.
- Record the exact test amounts in minor currency units and expected displayed totals before testing reports.

## Authentication and account tests

| ID | Scenario | Action | Expected result |
| --- | --- | --- | --- |
| AUTH-01 | Successful registration | Submit a unique valid name, email, and password. | Account is created; user enters the authenticated app area. |
| AUTH-02 | Duplicate email | Register using an existing email. | Account is not created; a clear duplicate-email error appears. |
| AUTH-03 | Invalid registration input | Omit required values or use invalid email/password input. | Submission is blocked or rejected with field-specific errors. |
| AUTH-04 | Successful sign in | Sign in with valid credentials. | Authenticated pages load and current-user details are available. |
| AUTH-05 | Incorrect sign in | Use a correct email with an incorrect password. | No session is created; response does not reveal which credential was wrong. |
| AUTH-06 | Protected access | Visit a protected API/page without a valid session. | Access is denied and the interface redirects or prompts for sign-in. |
| AUTH-07 | Sign out | Sign out, then refresh or revisit a protected page. | Session is cleared and protected data is unavailable. |

## Category tests

| ID | Scenario | Action | Expected result |
| --- | --- | --- | --- |
| CAT-01 | Create expense category | Add Food as an expense category. | It appears in the category list and expense transaction form. |
| CAT-02 | Create income category | Add Salary as an income category. | It appears only for income transactions. |
| CAT-03 | Update category | Rename Food or change its color. | Updated details appear consistently across the app. |
| CAT-04 | Invalid category | Submit blank/overlong name or invalid type. | Category is not saved; validation explains the problem. |
| CAT-05 | Archive category | Archive a category with old transactions. | History stays intact; the category is unavailable for new transactions unless restored. |
| CAT-06 | Other-user isolation | As User B, request or edit a User A category by guessed identifier. | The request is denied or behaves as if no record exists; no User A details leak. |

## Transaction tests

| ID | Scenario | Action | Expected result |
| --- | --- | --- | --- |
| TX-01 | Add expense | Add a valid Food expense with date, amount, and description. | It saves once, appears in the list, and decreases the selected-period balance. |
| TX-02 | Add income | Add a Salary income transaction. | It saves once and increases the selected-period balance. |
| TX-03 | Required validation | Submit with missing date, amount, type, or category. | The transaction is not saved; clear errors identify invalid fields. |
| TX-04 | Amount validation | Try zero, negative, non-numeric, and excessively large amounts. | Invalid values are rejected according to documented rules. |
| TX-05 | Type/category consistency | Submit an expense using an income category, or vice versa. | Backend rejects the mismatch even if browser controls are bypassed. |
| TX-06 | Edit transaction | Change an amount, category, or date. | List, overview totals, reports, and budget progress update correctly. |
| TX-07 | Delete transaction | Confirm deletion of a transaction. | It disappears; all affected totals recalculate correctly. |
| TX-08 | Cancel deletion | Open deletion confirmation and cancel. | No record or total changes. |
| TX-09 | Date filtering | View selected month and a custom date range. | Only transactions inside the requested range appear and totals match them. |
| TX-10 | Category/type filtering | Filter by Food and then by expense. | Results meet every active filter. |
| TX-11 | Pagination | Create more entries than one page shows and navigate pages. | No entries are repeated/missing; page totals and controls are correct. |
| TX-12 | Other-user isolation | As User B, read/update/delete a User A transaction using a guessed identifier. | Access is denied without exposing User A data. |

## Budget and report tests

| ID | Scenario | Action | Expected result |
| --- | --- | --- | --- |
| BUD-01 | Set a monthly budget | Save a Food budget for the selected month. | Exactly one Food budget is shown for that month. |
| BUD-02 | Update same budget | Save a new Food amount for the same month. | Existing budget changes rather than creating a duplicate. |
| BUD-03 | Budget calculation | Add Food expenses before/at/over the budget amount. | Spent, remaining, and over-budget values equal the expected integer-based calculation. |
| BUD-04 | Month separation | Switch months. | Budget and spending display only values for that month. |
| BUD-05 | Invalid budget | Set a budget on an income category or use invalid amount/month. | Backend rejects it with a clear error. |
| REP-01 | Monthly totals | Compare overview income, expenses, and balance with the known test records. | Totals are exactly correct and exclude prior-month data. |
| REP-02 | Category breakdown | Compare each report category amount with its known transactions. | Every category amount and total is correct. |
| REP-03 | Empty period | Select a period with no transactions. | The page shows zero/empty state; no error or misleading chart appears. |
| REP-04 | Currency display | Use amounts that include minor units. | Format is consistent and does not show floating-point artifacts. |

## Interface, reliability, and accessibility tests

| ID | Scenario | Action | Expected result |
| --- | --- | --- |
| UI-01 | Loading state | Slow or temporarily delay an API response. | Page indicates loading and does not show broken/old data as final. |
| UI-02 | Server error | Force a safe test API error. | A plain-language error and retry path appear; app does not crash. |
| UI-03 | Empty state | Use a new account with no categories or transactions. | Helpful next action is shown. |
| UI-04 | Keyboard form use | Navigate sign-in and transaction form with keyboard only. | Focus order is sensible; labels and buttons work. |
| UI-05 | Responsive layout | Test phone-width, tablet-width, and desktop-width viewports. | Navigation, forms, and tables remain usable without horizontal clipping. |
| UI-06 | Refresh persistence | Add data, refresh each main page, and revisit later. | Saved data persists and displayed totals remain correct. |

## Release gate

Do not treat the first version as complete until all authentication, ownership, transaction, budget, and report tests pass. Automate the high-risk backend cases first: unauthenticated access, cross-user access, invalid input, money totals, date filters, and one-budget-per-category/month.
