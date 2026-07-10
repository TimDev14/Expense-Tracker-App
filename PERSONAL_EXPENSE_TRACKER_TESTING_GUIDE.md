# Personal Expense Tracker: How to Develop and Run Functional Tests

This guide explains how testing should be developed alongside the application. It deliberately does not contain runnable code; use it as the blueprint when creating the test files.

## Testing layers

| Layer | What it checks | Recommended location |
| --- | --- | --- |
| Model tests | Database constraints, relationships, and helper calculations. | `backend/tests/models/` |
| Service tests | Pure business rules such as totals, budget progress, date filtering, and category/type compatibility. | `backend/tests/services/` |
| API tests | HTTP behavior, validation, authentication, authorization, and JSON response shapes. | `backend/tests/api/` |
| Component tests | Form errors, loading/empty/error views, filtering controls, and displayed summaries. | `frontend/src/**/__tests__/` or beside components. |
| User-flow tests | A browser-like register-to-transaction-to-report journey. | `frontend/e2e/` |
| Manual acceptance tests | Visual responsiveness, usability, and exploratory checks. | This directory’s test plan. |

## Backend test environment

Use `pytest` and Flask’s testing support. Create a dedicated Flask test configuration with a temporary SQLite database, test-only JWT secret, and testing mode enabled. The test database must be created before a test and removed/reset after it, so test data cannot affect development or production data.

Provide reusable test fixtures for: a Flask app, test client, database/session, User A, User B, an authenticated request identity for each user, categories, transactions, and budgets. Fixtures should contain predictable values so totals and response assertions are easy to understand.

Run tests in three useful scopes during development:

1. The focused test file after changing a model, endpoint, or calculation.
2. All backend tests before committing a feature.
3. The full backend and frontend suite before deployment.

## How to write each backend test

Use Arrange–Act–Assert.

1. **Arrange:** Build only the users and data necessary for the scenario.
2. **Act:** Call the model/service or send one API request using the test client.
3. **Assert:** Check the HTTP outcome, response body, database state, and any relevant calculated total.

Give test names that say what behavior is protected, such as a transaction belonging to another user cannot be updated, or a monthly report excludes transactions outside the selected month. Tests should verify observable behavior rather than internal implementation details.

For every new endpoint, add at least one success test, one invalid-input test, one unauthenticated test, and one cross-user authorization test. For every money calculation, choose values that expose rounding or boundary errors (zero spending, exactly at budget, and one smallest unit above budget).

## Frontend tests

Use a React testing tool such as Vitest together with React Testing Library. Test what a user sees and does: enter form values, submit, wait for success or error messages, change a filter, and confirm summary text updates. Mock API calls at the boundary rather than testing Flask internals from a component test.

Prioritize these frontend cases:

- Sign-in form validates errors and sends valid credentials.
- Protected routes redirect users without a session.
- Transaction form validates fields and displays backend errors.
- Transactions list renders loading, empty, populated, and error states.
- Changing month/category/type filters requests and presents the expected records.
- Budget cards explain on-track, at-limit, and over-budget states in text as well as color.

## End-to-end tests

Once the core app works, use a browser automation tool such as Playwright for a small number of critical flows. Keep these tests few and valuable because they are slower and more sensitive to interface changes.

The essential end-to-end flow is: register a fresh user → create an expense category → add an expense → set a budget → confirm overview and budget values → sign out → confirm protected data is inaccessible. Add an independent second-user isolation flow after that.

## Test data and safety rules

- Use invented emails and amounts only; never place personal financial data in test fixtures or screenshots.
- Make tests independent: each test creates its required state and can run in any order.
- Use test database transactions or cleanup fixtures so one test cannot affect another.
- Freeze or explicitly provide dates for date-sensitive tests; do not rely on the current calendar date.
- For money, assert integer minor-unit values at the backend and formatted values at the frontend.
- Do not disable authentication or authorization simply to make tests easier. Test the same protection that production uses.

## Development workflow

1. Read the relevant scenario in `PERSONAL_EXPENSE_TRACKER_TEST_PLAN.md` before implementing a feature.
2. Add the backend tests for the rules and failure cases first, or immediately alongside implementation.
3. Implement the smallest behavior needed to make the backend test pass.
4. Add the React component test for the user-facing result.
5. Run the focused tests, then the full relevant suite.
6. Mark the scenario passed in the test plan only after it passes reliably from a clean test database.
7. Add a regression test whenever you fix a defect.

## Coverage priorities

High coverage is useful, but confidence comes from testing risks. Protect these areas first: password and session handling, record ownership, amount validation, category/type matching, date-range calculations, budget uniqueness, monthly totals, and deletion recalculation. Add visual polish and chart tests only after the numbers and access controls are trustworthy.
