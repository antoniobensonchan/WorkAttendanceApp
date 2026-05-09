@echo off
echo ========================================
echo Git Repository Setup for WorkAttendanceApp
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo [1/5] Checking Git installation...
git --version
echo.

echo [2/5] Initializing Git repository...
if not exist .git (
    git init
    echo ✓ Git repository initialized
) else (
    echo ✓ Git repository already exists
)
echo.

echo [3/5] Adding files to staging...
git add .
echo ✓ Files added
echo.

echo [4/5] Creating initial commit...
git commit -m "Initial commit - Work Attendance Management System"
echo.

echo [5/5] Setup complete!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub.com
echo 2. Run these commands:
echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo Or use GitHub Desktop for easier management!
echo.
pause
