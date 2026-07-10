# Personal Expense Tracker: Build Guide

This is the recommended first app. It lets one signed-in user record money in and out, organize it by category, set budgets, and understand their monthly position. Build the smallest working version first; charts, recurring entries, and exports come after the core records are reliable.

## 1. Define the first release

### User goals

- Create an account and securely sign in.
- Add, edit, and delete income and expense transactions.
- Create and manage personal categories.
- Choose a month and see income, expenses, and the remaining balance.
- Set an expense budget per category for a month.
- See budget-versus-spending progress and a category breakdown.

### Keep out of the first release

- Bank-account connections and payments.
- Receipt uploads, recurring transactions, and CSV import/export.
- Multiple currencies, multiple wallets, shared household accounts, and push/email notifications.

Those features are useful later but each adds design and security work.

## 2. Choose the project layout

Create one root folder named `personal-expense-tracker`, with a `frontend` folder for React and a `backend` folder for Flask. Keep them independent: React owns the visual interface; Flask owns API rules and database access.

```
personal-expense-tracker/
├── README.md
├── .gitignore
├── frontend/
│   ├── package.json
│   ├── .env.example
│   └── src/
│       ├── api/                  # Requests to the Flask API
│       ├── components/           # Reusable interface pieces
│       │   ├── auth/
│       │   ├── expenses/
│       │   └── shared/
│       ├── context/              # Signed-in user state
│       ├── layouts/              # Public and authenticated page frames
│       ├── pages/                # Route-level screens
│       │   ├── auth/
│       │   └── expenses/
│       ├── schemas/              # Browser-side form validation
│       ├── styles/
│       └── utils/                # Currency and date display helpers
└── backend/
    ├── requirements.txt
    ├── .env.example
    ├── instance/                 # Local SQLite database; never commit it
    ├── migrations/               # Database-change history
    ├── tests/
    │   ├── api/
    │   ├── models/
    │   └── services/
    └── app/
        ├── models/
        ├── routes/
        ├── schemas/
        ├── services/
        ├── utils/
        ├── config.py
        ├── extensions.py
        └── __init__.py
```

## 3. Install the required tools and packages

Install a current supported Python version, Node.js, and npm before creating the project. Use a Python virtual environment for the backend so each project has isolated Python packages.

| Area | Package/tool | Purpose |
| --- | --- | --- |
| Frontend base | React, React DOM, Vite | React application and local development server. |
| Frontend routing | React Router | Pages such as Sign in, Overview, Transactions, Budgets, and Reports. |
| Frontend HTTP | Axios | Centralizes authenticated requests and error handling. |
| Forms | React Hook Form, Zod, Hook Form resolvers | Form state and immediate client-side validation. |
| Dates/charts | Day.js, Recharts | Date selection/formatting and report visuals. |
| Icons | Lucide React | Accessible interface icons. |
| Flask base | Flask, Flask-Cors | API application and allowed React-to-Flask requests during development. |
| Database | Flask-SQLAlchemy, Flask-Migrate | Database models and safe schema changes. |
| Authentication | Flask-JWT-Extended, bcrypt or argon2-cffi | Login tokens and secure password hashes. |
| Configuration | python-dotenv | Reads local environment variables without committing secrets. |
| Testing | pytest, pytest-flask | Automated backend functionality tests. |

SQLite is available through Python's standard library. Do not add a separate SQLite server for this project.

## 4. Design the database before screens

The database should have these tables/entities.

| Entity | Essential fields | Rules |
| --- | --- | --- |
| User | id, display name, email, password hash, default currency, timezone, created time | Email must be unique; password is always a secure hash. |
| Category | id, user id, name, type, color/icon, active state | A category belongs only to one user and is income or expense, never both. |
| Transaction | id, user id, category id, amount in minor units, type, date, description, created/updated time | The transaction and chosen category must belong to the same user; transaction type must match category type. |
| Budget | id, user id, category id, month, amount in minor units | Only one budget per user/category/month. Budgets apply to expense categories. |

### Important money rule

Store amounts as integers in the currency's smallest unit, such as cents. For example, store $12.50 as 1250 rather than a decimal floating-point value. This avoids rounding errors in totals and budgets. Decide on a default currency for each user; for a first version, let it be selected during profile setup but do not automatically convert currencies.

### Ownership rule

Every database lookup and write must be scoped to the authenticated user. A person must never retrieve or change another person’s transaction by modifying an address in the browser.

## 5. Plan the backend API

Use a consistent API prefix such as `/api`. Flask route modules should be grouped by responsibility: authentication, categories, transactions, budgets, reports, and profile.

| API group | Required operations |
| --- | --- |
| Authentication | Register, sign in, get current user, sign out/session invalidation strategy. |
| Profile | Read and update display name, default currency, and timezone. |
| Categories | Create, list, update, archive, and delete categories where safe. |
| Transactions | List with month/date/category/type filters; create, retrieve, update, delete. |
| Budgets | List by month, create/update a category budget, remove a budget. |
| Reports | Month totals, category totals, budget progress, and recent transactions. |

For every endpoint, define the accepted request fields, success response fields, validation errors, and authorization behavior before implementing it. Return predictable JSON and suitable HTTP outcomes for success, invalid input, missing records, authentication failure, and permission denial.

## 6. Plan the React application

### Pages

| Page | Responsibility |
| --- | --- |
| Sign up / Sign in | Registration, login, clear validation errors, and redirect into the app. |
| Overview | Selected-month income, expenses, balance, recent transactions, budget alerts, and one small chart. |
| Transactions | Filterable, paginated list with add/edit/delete transaction form. |
| Budgets | Choose month, set category budgets, and see amount spent versus remaining. |
| Reports | Category spending breakdown and date-range summary. |
| Categories | Add, rename, archive, or remove categories. |
| Settings | Profile, currency, timezone, and sign-out. |

### Reusable components

Create focused components rather than one very large page: navigation sidebar/header, protected-route guard, transaction form, transaction table/row, category selector, date/month picker, budget progress card, summary card, confirmation dialog, loading indicator, empty state, and error message.

The application should centralize API requests in `src/api` and currency/date formatting in `src/utils`. Pages should not duplicate request logic or money formatting rules.

## 7. Build in milestones

### Milestone 1: foundation

Set up the two applications, version control exclusions, environment-variable templates, Flask configuration, CORS for the local React origin, and a health-check endpoint. Confirm React can reach Flask.

### Milestone 2: accounts and protection

Create users, secure password hashing, sign-up and sign-in flows, JWT protection, and a current-user endpoint. Build the React authentication screens and protected app layout. Test that protected requests fail without a valid session.

### Milestone 3: categories and transactions

Create the category and transaction data models, migrations, validation, and CRUD APIs. Build the Transactions and Categories pages. Confirm users can only see their own data.

### Milestone 4: monthly overview

Add selected-month filters and backend summary calculations. Build overview cards and recent-transaction display before adding charts.

### Milestone 5: budgets and reports

Add budgets, budget-progress calculations, category totals, and reports. Add one chart only after the numbers are correct in text/table form.

### Milestone 6: polish and release preparation

Add accessible error/empty/loading states, responsive layouts, tests, logging, production environment variables, backups, and deployment configuration.

## 8. Security and quality checklist

- Never put Flask secret values, JWT secrets, database files, or real tokens in Git.
- Hash passwords with a dedicated password-hashing library; never encrypt or store them as plain text.
- Validate input in Flask even if React validates it first.
- Enforce ownership on every record access.
- Restrict CORS to the actual frontend origin in production.
- Add rate limiting to registration and login before public release.
- Confirm delete actions with the user, show useful validation messages, and add loading/empty/error states.
- Back up the SQLite file. SQLite is excellent locally and for a small single-server app; migrate to PostgreSQL if many concurrent users or servers are needed.

## 9. Recommended first working slice

Do not start with graphs. Complete this journey first: register → sign in → create an expense category → add a transaction → list it after refresh → edit it → delete it → verify a second user cannot access it. That proves the frontend, API, database, security, and user experience are connected correctly.

## 10. Initial setup, explained

The repository now uses `frontend` and `backend` as the project roots described above. They run independently in two terminals because Vite serves the browser application while Flask serves JSON data.

### Frontend setup and commands

Copy `frontend/.env.example` to `frontend/.env` before development. `VITE_API_BASE_URL` is intentionally public: Vite exposes only variables prefixed with `VITE_` to the browser, so never store a password, JWT secret, or database URL in this file.

Run these commands from `frontend`:

```bash
npm install
npm run dev
```

Vite prints the local URL (normally `http://localhost:5173`). `npm run build` produces the deployable browser bundle in `frontend/dist`; it should pass before a release. `npm run test` runs the Vitest unit suite. Playwright is included for later end-to-end tests, but its browser binaries are deliberately not downloaded until tests are introduced (`npx playwright install`).

The installed frontend packages have distinct jobs:

| Package | Why it is included |
| --- | --- |
| `react`, `react-dom`, `vite` | Render the application and provide a fast local development/build workflow. |
| `react-router-dom` | Maps URLs to public and authenticated pages. |
| `axios` | Provides one API client with a base URL, token handling, and consistent error conversion. |
| `react-hook-form`, `zod`, `@hookform/resolvers` | Keep forms responsive and apply the same clear validation rules before requests are sent. |
| `dayjs` | Parses, selects, and formats transaction dates and selected months. |
| `recharts` | Draws the report chart only after the text totals are correct. |
| `lucide-react` | Supplies consistent, accessible SVG icons. |
| `vitest`, Testing Library, `jsdom` | Test components from a user's perspective without starting a real browser. |
| `@playwright/test` | Supports the few high-value browser flows described in the testing guide. |

### Backend setup and commands

Copy `backend/.env.example` to `backend/.env`, replace both secret placeholders with unique random values, and never commit that file. `DATABASE_URL` has a local SQLite default; the resulting database is stored in `backend/instance` and is ignored by Git.

Create and activate a virtual environment, then install the dependencies:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run.py
```

Flask should answer `GET http://127.0.0.1:5000/api/health` with `{ "status": "ok" }`. That endpoint is intentionally public; it confirms the server is reachable but does not expose user or financial data. Once the API is running, the frontend can call it through the URL in its `.env` file.

The backend is intentionally organized around an application factory (`app.create_app`). This makes the same application easy to run locally, configure for tests, and deploy without duplicated setup. Flask extensions are initialized in `extensions.py`, then connected to the application in the factory. Routes, models, validation schemas, and calculation services stay in separate packages so HTTP code does not become the place where all business logic lives.

## 11. How the core functionality fits together

### Authentication and privacy

Registration validates a display name, unique email, and sufficiently strong password. The backend hashes the password with `bcrypt`; it never stores the submitted password. A successful sign-in returns or sets a JWT-based session according to the chosen storage strategy. The React API client attaches that session only to protected requests, while a protected-route component redirects signed-out visitors to sign in.

An authenticated identity is not enough on its own. Every category, transaction, and budget query must include the current user's ID. For example, updating `/api/transactions/42` must first load transaction 42 *for the current user*; a record belonging to someone else should return a non-disclosing not-found/forbidden response. This ownership check belongs on every read, update, and delete endpoint, not only in the visible UI.

### Categories and transactions

Categories make reporting meaningful. A category has one type (`income` or `expense`), a name, an optional color/icon, and an active state. Archiving preserves historical transactions but removes the category from new-entry choices. Deleting should only be allowed when it cannot damage history, or it should require a deliberate migration of existing transactions.

When a transaction is created or edited, validate all fields on the server: date, positive integer minor-unit amount, type, category ownership, and category/type match. Store `1250` for a $12.50 amount. The browser converts a user-friendly decimal input into minor units at the API boundary, and shared formatting helpers convert it back for display. This keeps totals exact and prevents floating-point artifacts.

### Monthly overview, budgets, and reports

The selected month must be passed to both transaction lists and summary endpoints in a consistent format such as `YYYY-MM`. The backend calculates income, expenses, and balance from records inside that month; it should not trust a browser-provided total. Recent transactions are a limited, date-sorted subset of the same owned records.

A budget is an expense-category limit for one month. Its uniqueness rule is `(user_id, category_id, month)`, so saving a budget for the same category and month updates the existing value rather than producing duplicates. Budget progress is calculated from that category's expense transactions in the matching month: spent, remaining (`budget - spent`), and status (on track, at limit, or over budget). The Reports page reuses these server-side totals for category breakdowns and optional charts.

## 12. Implementation order and definition of done

1. **Foundation:** Start both servers, call `/api/health`, and confirm browser CORS allows only the configured local frontend origin.
2. **Accounts:** Add the User model, migration, registration/sign-in/current-user endpoints, and the sign-in screens. Test invalid and duplicate credentials as well as a request with no token.
3. **Categories and transactions:** Add database constraints, server validation, owned CRUD endpoints, and the matching forms/lists. Test a second user cannot access guessed IDs.
4. **Overview:** Add one month-query service, summary endpoint, summary cards, and a recent-transactions view. Verify totals with known integer amounts before designing charts.
5. **Budgets and reports:** Add the budget uniqueness constraint, progress calculation, category totals, and the reports/budgets pages. Test empty months and exactly-at-budget values.
6. **Release readiness:** Add loading, error, empty, keyboard-accessible, and mobile states; run the complete backend/frontend suites; then configure production secrets, restricted CORS, backups, and deployment.

For each milestone, a feature is done only when its request validation, authentication/ownership behavior, success path, and meaningful error/empty state are covered by the scenarios in `PERSONAL_EXPENSE_TRACKER_TEST_PLAN.md`. This prevents attractive screens from masking incorrect financial totals or privacy holes.
