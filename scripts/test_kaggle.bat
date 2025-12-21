@echo off
echo Testing Kaggle API setup...

echo Checking for kaggle.json...
if exist "%USERPROFILE%\.kaggle\kaggle.json" (
    echo ✅ Found kaggle.json in user directory
) else if exist "kaggle.json" (
    echo ℹ️  Found kaggle.json in project directory
) else (
    echo ❌ kaggle.json not found!
    goto error
)

echo.
echo Testing Kaggle API...
kaggle datasets list -s "credit card" --max-size 1
if %errorlevel% equ 0 (
    echo ✅ Kaggle API is working!
) else (
    echo ❌ Kaggle API test failed!
    goto error
)

goto end

:error
echo.
echo Please setup Kaggle API:
echo 1. Get kaggle.json from https://www.kaggle.com/account
echo 2. Run: scripts\setup_kaggle.bat
echo.

:end
pause