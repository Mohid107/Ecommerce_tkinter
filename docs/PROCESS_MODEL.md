# Software Process Model: Agile/Scrum

## Methodology Selection

We chose the **Agile/Scrum** methodology for the development of the ShopEasy E-Commerce Application. This approach allows for iterative development, frequent feedback loops, and the ability to adapt to changing user requirements (such as the pivot from a simple refactor to a full UI overhaul).

## Process Implementation

### 1. Sprints & Cycles

The project was divided into logical cycles (simulating 2-week sprints):

- **Sprint 1: Foundation & Setup** (Initial setup, GitHub tracking, DB connection).
- **Sprint 2: Refactoring & Architecture** (Transition to MVC, Dependency Injection).
- **Sprint 3: UI/UX Enhancements** (Hero section, Profile settings, Treeview Cart).
- **Sprint 4: Quality Assurance & DevOps** (Automated GUI testing, CI/CD implementation).

### 2. User Story Creation

Requirements were treated as User Stories, derived from stakeholder (User) prompts.

- _Example Story_: "As a user, I want a professional cart layout so I can see item totals clearly."
- _Acceptance Criteria_: Defined implementation plans (e.g., "Use ttk.Treeview", "Show columns for Price/Qty").

### 3. Task Tracking

We utilized a living **Task List** (`task.md`) to track progress.

- Tasks were broken down into granular items.
- Status was tracked (Todo `[ ]`, In-Progress `[/]`, Done `[x]`).
- This replaced a traditional Kanban board but served the same purpose of visibility.

### 4. Daily Standups (Simulated)

At the start of each session (Task Boundary), we assessed:

- **What was done**: Reviewed previous tool outputs and git history.
- **What is planned**: Defined the scope for the current interaction.
- **Blockers**: Identified issues like "AttributeError in theme" and pivoted immediately to fix them.

### 5. Sprint Review & Retrospective

- **Walkthroughs**: The `walkthrough.md` artifact served as our Sprint Review document, summarizing what was built and verifying it works.
- **Adaptation**: When GUI crashes occurred or tests failed, we halted new feature work to stabilize the build (a core Agile principle).
