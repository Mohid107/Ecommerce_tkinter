# Code Review Checklist

Use this checklist during peer reviews to maintain high code quality standards.

## 1. Functionality

- [ ] Does the code accomplish the ticket's goal?
- [ ] Are edge cases handled? (e.g., empty inputs, network failures)
- [ ] Is error handling robust? (No bare `except:`, proper user feedback)

## 2. Architecture & Design

- [ ] Does it follow the **MVC Pattern**? (Logic in Services, UI in Views)
- [ ] Is **Dependency Injection** used correctly? (No global state access)
- [ ] Are constants used for strings/magic numbers? (`src/core/constants.py`)

## 3. Style & Cleanliness

- [ ] Is the code PEP8 compliant? (Run `flake8`)
- [ ] Are variable/function names descriptive?
- [ ] Is dead code removed?

## 4. Testing

- [ ] Are new Unit Tests added for logic?
- [ ] Are GUI Tests added for new screens?
- [ ] Do all tests pass locally? (`pytest`)

## 5. Security

- [ ] No hardcoded credentials?
- [ ] Input validation present? (SQL Injection prevention handled by parameterized queries in `db.py`)
