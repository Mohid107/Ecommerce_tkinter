# Deployment Guide

## System Requirements

- **OS**: Windows 10/11
- **Database**: SQL Server (Express or Standard)
- **Runtime**: Python 3.8+ (if running from source) OR No runtime needed (if using `.exe`)

## Installation

### Option 1: Standalone Executable (Recommended for Users)

1. Download `ShopEasy.exe` from the GitHub Releases page.
2. Ensure you have network access to the SQL Server.
3. Double-click `ShopEasy.exe` to launch.

### Option 2: Running from Source (For Developers)

1. Clone the repository.
2. Run the installer script:
   ```cmd
   install_dependencies.bat
   ```
3. Run the application:
   ```cmd
   run_app.bat
   ```

## Build Process

To create a new executable:

1. Install build dependencies: `pip install pyinstaller`.
2. Run the build script:
   ```cmd
   python build.py
   ```
3. The output will be inside the `dist/` folder.

## Troubleshooting

- **Crash on Start**: Verify SQL Server is running and `src/data/db.py` connection string is correct.
- **Missing DLLs**: Ensure Visual C++ Redistributable is installed if running on fresh Windows.

## Updates

Currently, updates are manual. Please check the GitHub repository for the latest `ShopEasy.exe` release.
