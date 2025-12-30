# Code Review Examples

Documenting past review findings to share knowledge and prevent recurrence.

## Example 1: Architecture Violation

**Issue**: Directly calling `db.execute` from `LoginView`.
**Review Comment**: "Views should not interact with the DB directly. Please move this logic to `UserService`."
**Outcome**:

- Code refactored to use `UserService.login()`.
- **Benefit**: UI is now testable with mocked service; DB logic is reusable.

## Example 2: Missing Constants

**Issue**: `tk.Label(text="ShopEasy")` used in multiple places.
**Review Comment**: "Please move the app title to `AppConstants` in `src/core/constants.py`."
**Outcome**:

- Changed to `AppConstants.APP_TITLE`.
- **Benefit**: Changing the app name now requires only one edit.

## Example 3: Error Handling

**Issue**: Application crashed when `theme.py` was missing a Font definition.
**Review Comment**: (Post-Incident) "We need to ensure all theme attributes used in Views are actually defined."
**Outcome**:

- Added `Fonts.TITLE` and `Fonts.SUBTITLE` to `theme.py`.
- **Benefit**: Prevented runtime `AttributeError`.

## Example 4: Security

**Issue**: SQL String concatenation in `User.py`.
**Review Comment**: "Use parameterized queries `?` instead of f-strings to prevent SQL Injection."
**Outcome**:

- Changed `f"SELECT * FROM Users WHERE name='{name}'"` to `execute("SELECT * FROM Users WHERE name=?", (name,))`
- **Benefit**: Secured application against basic attacks.
