# Lehman's Laws of Software Evolution Analysis

This project demonstrates several of Lehman's Laws, illustrating the natural evolution of software systems.

## 1. Law of Continuing Change (I)

> _"A system must be continually adapted or it becomes progressively less satisfactory."_

**Observation**:
The initial E-Commerce app functioned correctly but lacked visual appeal and modern features. The User feedback ("Home screen has disappeared", "Make cart professional") drove **Continuing Change**.

- **Evidence**: We didn't just fix bugs; we evolved the UI from simple Frames to complex `Treeview` layouts and Hero sections to meet increasing user expectations for "attractiveness" and "professionalism."

## 2. Law of Increasing Complexity (II)

> _"As a system evolves, its complexity increases unless work is done to maintain or reduce it."_

**Observation**:
Adding new features (Password Update, Checkout Validations, Hero Banners) naturally increased code size and complexity.

- **Counter-Measure**: To combat this, we applied **Refactoring** (MVC Pattern).
- **Evidence**: Before adding the complex Checkout form, we extracted logic into `OrderService`. Without this structure, `run.py` would have become unmaintainable. Defining `AppConstants` and `ViewNames` reduced the entropy of magic strings.

## 3. Law of Feedback System (VIII)

> _"Evolving processes constitute multi-level, multi-loop feedback systems."_

**Observation**:
Our development process relied heavily on feedback loops at multiple levels:

- **Level 1 (Code)**: Linter (flake8) provided immediate feedback on syntax.
- **Level 2 (Function)**: Automated Tests (pytest) provided feedback on logic correctness.
- **Level 3 (User)**: The User provided qualitative feedback ("Good", "Implement now", "Home page appears as soon as we login"), which immediately altered the backlog.
- **Evidence**: The rapid iteration from "Refactoring" to "UI Polish" to "CI/CD" was driven entirely by these feedback loops closing successfully.
