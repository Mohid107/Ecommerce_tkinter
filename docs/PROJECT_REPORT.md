# Semester Project Report: ShopEasy E-Commerce System

**Project Title**: ShopEasy Desktop Application
**Team Roles**:

- **Lead Developer**: [User Name] (Architecture, Core Logic, Testing)
- **AI Assistant**: Antigravity (Refactoring, CI/CD Setup, Documentation)

---

## 1. Software Process Model

**Model Selected**: Agile/Scrum

**Justification**:
We selected Agile/Scrum because the project requirements involved significant evolution and discovery. Initially, the goal was simple refactoring, but it evolved into a complete UI overhaul and architectural restructuring.

- **Iterative Development**: We worked in "cycles" (Task Boundaries), delivering working increments (e.g., Login View, then Home View, then Cart).
- **Adaptability**: When initial GUI tests failed due to widget hierarchy issues, we pivoted immediately to fix the test harness rather than following a rigid plan.
- **Feedback Loops**: Constant user feedback ("Implement this now", "Make it look professional") drove the backlog priorities.

## 2. Software Process Improvement (SPI)

**Implementation**: Yes, an SPI program was executed to transition from a "Legacy" to an "Engineered" state.

- **Legacy State**: The original application was a monolithic script (`run.py` mixed with business logic), harder to maintain and test.
- **Improved State**:
  - **Architecture**: Enforced MVC (Model-View-Controller) to decouple UI from logic.
  - **Quality**: Introduced automated testing (`pytest`), reducing regression risk.
  - **DevOps**: Implemented CI/CD (`GitHub Actions`), ensuring ensuring every commit is buildable.
- **Metric**: reduced "Change Risk" from High (manual testing) to Low (automated suites).

## 3. Version Control

**Tool**: Git & GitHub

**Implementation**:

- **Repository**: Hosted on GitHub (`Ecommerce_tkinter`).
- **Workflow**: Feature Branch / Trunk-based development. Changes were staged, committed with descriptive messages (e.g., _"Refactor UserService to use custom exceptions"_), and pushed relative to task completion.
- **CI Integration**: The `.github/workflows/python-test.yml` file is triggered on every `push`, ensuring the repository state is always valid.

## 4. Lehman’s Laws of Software Evolution

The project serves as a case study for Lehman's Laws:

1.  **Law of Continuing Change**: The application had to evolve from a basic prototype to a "Professional" tool to remain useful. We updated the UI to use `Treeview` and modern styling to satisfy this need.
2.  **Law of Increasing Complexity**: Adding features like "Password Reset" and "Validation" increased entropy. We countered this by Refactoring (Move Class) and creating a dedicated `src/services` layer.
3.  **Law of Feedback Systems**: The development was driven by multi-level feedback: Linter (Syntax), Pytest (Logic), and User (Requirements).

## 5. Software Deployment Management

**Strategy**: Standard Python Packaging & Standalone Executable.

**Artifacts**:

- **`setup.py`**: Allows the application to be installed as a python package (`pip install .`).
- **`scripts/build.py`**: Automates `PyInstaller` to create a single-file `ShopEasy.exe` for end-users, handling asset bundling (`media/`).
- **`scripts/install_dependencies.bat`**: Simplifies environment setup for new developers.
- **Documentation**: A detailed `docs/DEPLOYMENT.md` guide was created to assist users with installation and troubleshooting.

## 6. Refactoring & Legacy Key Removal

**Approach**: "Strangler Fig" pattern (simulated).

- We gradually moved logic out of the global scope in `run.py` into `src/services` and `src/views`.
- **Global Variable Elimination**: Replaced global `current_user` with `UserService` instance state, injected via Dependency Injection.
- **Hardcoded Strings**: Moved all UI text and configuration to `src/constants.py`.
- **Legacy Directories**: Deleted `src/data` (old CSV/DB mixed code) and `src/gui` (old monolithic files) after verifying the new `src/models` and `src/views` worked correctly.

## 7. Unit Testing

**Framework**: `pytest`

**Scope**:

- **Services**: Verified `UserService` and `CartService` logic (e.g., successful login, adding items, stock validation).
- **Exceptions**: Verified that `DatabaseError` is raised correctly after retries.
- **Models**: Verified data integrity in `User` and `Product` models.

## 8. Automated Testing

**Implementation**: Automated GUI Testing with `unittest.mock`.

- We avoided complex tools like Selenium (web) and used `tkinter` mocking.
- **Tests**: `tests/test_gui.py` simulates a user clicking "Login". It verifies that the `controller.show_view` method is called with the correct argument (`ViewNames.HOME`), proving the flow works without launching a physical window.

## 9. Exception Handling

**Concepts Applied**:

- **Custom Hierarchy**: Created `src/exceptions.py` defining `AppError`, `DatabaseError`, `AuthenticationError`.
- **Resilience**: Implemented **Retry Logic** in `src/db.py`. The app attempts to connect to SQL Server 3 times before giving up, handling transient network glitches.
- **Logging**: All exceptions are logged to `app.log` via `src/logger.py` for post-mortem analysis, while the User sees a friendly `messagebox`.

## 10. Peer Reviews

**Process**:

- **Checklist**: We utilized `docs/CODE_REVIEW_CHECKLIST.md` ensuring code met Architecture and Security standards.
- **Artifacts**: A `docs/code_reviews.csv` log was maintained to track reviews.
- **Impact**: Reviews caught critical issues, such as missing Font definitions in `theme.py` and SQL injection risks, which were fixed before the code was merged.

## 11. Learning Outcome

- **Technical**: Mastery of Python application structuring, CI/CD pipelines, and automated UI testing.
- **Process**: Understanding that "Agile" is not just meetings, but a way of building software that embraces change (Refactoring) while maintaining stability (Testing).
