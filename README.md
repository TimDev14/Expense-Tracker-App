# Ledgerly: A Beginner-Friendly Personal Expense Tracker

Ledgerly is a small full-stack web application for recording the money you earn and spend. It is built as a learning project, but its structure follows the same separation used by larger applications: a browser interface asks an API for data, and the API safely stores that data in a database.

## What problem does it solve?

It is easy to lose track of small purchases, monthly bills, and how much money remains after expenses. Ledgerly lets each person create a private account, make categories such as **Salary**, **Food**, and **Transport**, record transactions, set monthly spending limits, and view totals for a selected month.

Money is stored as an integer number of the smallest currency unit. For example, `$12.50` is stored as `1250` cents. Computers can add integers exactly, while decimal numbers can sometimes introduce tiny rounding mistakes.

## The two halves of the project

```
frontend/  → React application that runs in the browser
backend/   → Flask application that provides JSON data and talks to SQLite
```

When you click **Add transaction**, the frontend converts the typed amount to cents and sends a request to Flask. Flask validates it, checks that the selected category belongs to the signed-in user, saves it, and returns JSON. React then reloads the visible list.

## What you can do

- Register and sign in with an email address and password.
- Create income and expense categories.
- Add, list, and delete transactions for a month.
- Archive categories with history rather than accidentally deleting that history.
- Set one expense budget per category per month.
- See monthly income, expenses, balance, recent records, and category spending totals.
- Update the display name, currency code, and timezone.

## Important folders explained

### Backend

- `backend/run.py` starts the development server.
- `backend/app/__init__.py` creates Flask and connects routes, database support, CORS, and JWT authentication.
- `backend/app/models/` describes database tables: `User`, `Category`, `Transaction`, and `Budget`.
- `backend/app/routes/` contains URL handlers. They should stay small and hand calculations to services.
- `backend/app/services/finance.py` contains ownership lookups, monthly totals, and budget progress calculations.
- `backend/app/schemas/validation.py` checks data sent by the browser before it reaches the database.
- `backend/tests/` contains automated checks for public health, authentication, and user isolation.

### Frontend

- `frontend/src/main.jsx` starts React and supplies routing plus signed-in user state.
- `frontend/src/App.jsx` maps browser URLs to pages.
- `frontend/src/api/client.js` is the one place that configures calls to Flask and adds the access token.
- `frontend/src/context/` remembers the current user while the tab remains open.
- `frontend/src/pages/` are complete screens; `components/` holds reusable smaller pieces.
- `frontend/src/utils/format.js` converts stored minor-unit amounts into readable currency.

## Running it locally

Open two terminals. The apps run separately during development.

### 1. Start the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

The API starts at `http://127.0.0.1:5000`. Open `http://127.0.0.1:5000/api/health` and you should see `{"status":"ok"}`.

Create `backend/.env` from the example values and replace `SECRET_KEY` and `JWT_SECRET_KEY` with long random values before sharing or deploying the app. The local SQLite database is created inside `backend/instance/`.

### 2. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Vite prints a local address, usually `http://localhost:5173`. The frontend `.env` file points to the Flask API with `VITE_API_BASE_URL=http://127.0.0.1:5000/api`.

## A simple first-use walkthrough

1. Visit the Vite address and choose **Sign up**.
2. Create an account with a password of at least eight characters.
3. Add an expense category such as `Food`.
4. Open **Transactions**, choose `Food`, enter an amount and date, then click **Add**.
5. Return to **Overview** to see the monthly expense total.
6. Open **Budgets**, choose `Food`, set a limit, and compare what you spent with the limit.

## Privacy and security basics

Passwords are hashed with `bcrypt`; the original password is never stored. Signing in creates a JWT access token. Protected endpoints require that token and every category, transaction, and budget database query is limited to the current user. Guessing another record ID therefore returns “not found” instead of exposing somebody else’s finances.

For a production release, use strong secret values, HTTPS, a production WSGI server, a backed-up database, rate limiting for login/registration, and a more durable token/session strategy. Never commit real secret values or a real user database to Git.

## Tests

Run backend tests with:

```bash
cd backend
pytest
```

Run frontend checks with:

```bash
cd frontend
npm run lint
npm test
npm run build
```

The tests are intentionally focused on the risky behavior first: authentication and ensuring one user cannot modify another user's transaction.
