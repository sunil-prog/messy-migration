# CHANGES.md

## Overview
This document explains the changes made to refactor the original `app.py` and `init_db.py` into a secure, maintainable, and production-ready codebase while keeping the same API functionality.

---

## 1. Code Organization (25%)

### Original
- `app.py` contained both HTTP route definitions **and** all database queries.
- Single global SQLite connection reused for all requests (`check_same_thread=False`), risking concurrency issues.
- No clear separation between routing, business logic, and database access.
- `init_db.py` contained hardcoded inserts and table creation logic.

### Changes Made
- Split responsibilities into two clear layers:
  2. **Service Layer** – `user_service.py` handles input validation, business logic, and calls DB layer.
  3. **Database Layer** – `DatabaseOps.py` contains all database access functions using parameterized queries.
- Moved `users.db` file into a `Database/` directory for structural clarity.
- Renamed `init_db.py` to `DatabaseIntializer.py` for clear naming
- `DatabaseIntializer.py` now creates the schema with proper constraints and hashed sample passwords.

**Reasoning:**  
Separation of concerns improves maintainability, testability, and scalability.

---

## 2. Security Improvements (25%)

### Original
- SQL queries used f-string interpolation, vulnerable to SQL injection.
- Passwords stored in plain text.
- No input validation for email or required fields.
- No unique constraint on email addresses.

### Changes Made
- All queries now use **parameterized SQL** (`?` placeholders).
- Passwords hashed with `werkzeug.security.generate_password_hash()` and verified using `check_password_hash()`.
- Added **email format validation** using validator package
- Added `UNIQUE` constraint to email column in `users` table.
- Added handling for duplicate email errors (`sqlite3.IntegrityError`).

**Reasoning:**  
Eliminates SQL injection risk, secures user passwords, and enforces data integrity.

---

## 3. Best Practices (25%)

### Original
- Routes returned plain strings instead of JSON for many endpoints.
- No consistent HTTP status codes (`200 OK` returned even for errors).
- No central error handling pattern.
- DB connection kept open for entire app runtime.

### Changes Made
- Routes now return consistent JSON responses.
- Added proper HTTP status codes:
- `201 Created` for successful creation
- `400 Bad Request` for invalid input or duplicate email
- `404 Not Found` for missing records
- `401 Unauthorized` for failed login
- `500 Internal Server Error` for DB errors
- Each DB operation opens/closes its own connection via `with get_connection()` to prevent locking.
- Added `timeout=10` in `sqlite3.connect()` to reduce `"database is locked"` errors.

**Reasoning:**  
Improves API reliability, predictability, and concurrency safety.

---

## 4. Documentation (25%)

### Original
- No docstrings or inline comments.
- No explanation of design choices.

### Changes Made
- Added docstrings to each file explaining its role.
- Added inline comments in complex areas.
- Created this `CHANGES.md` file documenting:
- All changes made
- Justification for architectural decisions
- Security and best practice improvements
- Clear folder structure:
    project/
    ├── app.py
    ├── Services/
    │ └── UserServices.py
    ├── Database/
    │ ├── DatabaseIntializer.py
    │ ├── DatabaseOps.py
    │ └── users.db
    ├── CHANGES.md
    ├── README.md
    └── requirements.txt


---

## 5. Additional Improvements
- Added sample users with **hashed passwords** in `DatabaseIntializer.py`.
- Improved maintainability by centralizing error handling in `UserServices.py`.
- Removed all sensitive `print()` debug logs from production code.

---

## 6. Trade-offs
- Still using SQLite for simplicity — not ideal for high-concurrency production use.
- Schema changes require dropping/recreating table in SQLite (no migration tool yet).
- Validation is lightweight — deeper checks (e.g., DNS lookup for email) left for future work.

---

## 7. Summary
This refactor:
- Modularized the code into layers (routes, service, DB, validation)
- Fixed SQL injection & password security issues
- Added proper validation, error handling, and status codes
- Improved structure and documentation without changing API behavior

## 7. AI Assistance Disclosure
You are permitted to use AI assistants (ChatGPT, GitHub Copilot, etc.) as you would any other tool.  
For this refactor:

**Tools Used:**
- **ChatGPT (OpenAI)** — Used for guidance and generating initial refactored code patterns.

**Purpose:**
- Provided secure coding practices (parameterized SQL, password hashing).
- Suggested validation improvements.

**Modifications Made:**
- Some AI suggestions (e.g., full Blueprint-based routes structure) were **partially adopted**;
- Regex and validation logic were adjusted manually for project constraints. AI suggested regex but I used Validator package.
