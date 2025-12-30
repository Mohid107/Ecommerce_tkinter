# Software Process Improvement (SPI)

This document tracks the evolution of our development process and the improvements implemented to ensure quality and maintainability.

## 1. Initial State (Legacy Process)

- **Architecture**: Monolithic `run.py` containing GUI, Business Logic, and DB calls.
- **Testing**: Manual verification only. No automated test suite.
- **Build**: No build process. Ran directly from source.
- **Deployment**: Manual copy-paste. No CI/CD.
- **Issues**: High coupling made adding features (like a new Home screen) risky. Global variables caused state issues.

## 2. Improved Process

We implemented a structured SPI program focusing on modularity and automation.

### Architecture Improvement

- **Action**: Refactored to **MVC (Model-View-Controller)** pattern.
- **Outcome**: Separated concerns. Views (`src/gui/views`) handle display, Services (`src/core/services`) handle logic.
- **Benefit**: Changing the Login flow to redirect to Home instead of Products required changing only 1 line in `LoginView.py`, with no risk to DB logic.

### Quality Assurance Improvement

- **Action**: Implemented **Automated Testing** using `pytest` and `unittest.mock`.
- **Metrics**:
  - Unit Tests: 27 tests covering Logic/DB.
  - GUI Tests: 8 tests covering User Flows.
  - Coverage: Verified critical paths without manual intervention.
- **Benefit**: Caught `ttk.Frame` vs `tk.Frame` inheritance issues immediately during test runs.

### DevOps Improvement

- **Action**: Established **CI/CD Pipeline** with GitHub Actions.
- **Steps**: Linting (`flake8`), Testing (`pytest`), Build (`pyinstaller`).
- **Benefit**: Ensures that every commit is buildable and passes tests on a clean Windows environment.

## 3. Impact Analysis

| Metric               | Legacy Process               | Improved Process             |
| :------------------- | :--------------------------- | :--------------------------- |
| **Defect Detection** | Post-Release (Runtime Crash) | Pre-Commit (Local Test) & CI |
| **Deploy Time**      | Manual & Error Prone         | Automated & Reproducible     |
| **Code Coupling**    | High (Spaghetti Code)        | Low (Dependency Injection)   |
| **Feature Velocity** | Slow (High Risk of Breakage) | Fast (Stable Foundation)     |
