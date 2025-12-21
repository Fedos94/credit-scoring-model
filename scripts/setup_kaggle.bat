@echo off
echo Setting up Kaggle API...

if exist kaggle.json (
    echo Found kaggle.json, copying to Kaggle directory...
    
    # Create .kaggle directory in user folder
    if not exist "%USERPROFILE%\.kaggle" mkdir "%USERPROFILE%\.kaggle"
    
    # Copy kaggle.json
    copy kaggle.json "%USERPROFILE%\.kaggle\"
    
    echo ✅ Kaggle API configured successfully!
) else (
    echo ❌ kaggle.json not found in project root!
    echo Please create kaggle.json with your Kaggle API credentials.
)

pause