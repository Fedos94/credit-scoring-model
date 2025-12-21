# Kaggle API Setup

## Step 1: Get Kaggle API Credentials

1. Go to https://www.kaggle.com/
2. Click on your profile picture → Settings
3. Scroll to "API" section
4. Click "Create New API Token"
5. This will download `kaggle.json`

## Step 2: Place kaggle.json

### Option A: Automatic setup
1. Place `kaggle.json` in the project root folder
2. Run: `scripts\setup_kaggle.bat`

### Option B: Manual setup
1. Create folder: `%USERPROFILE%\.kaggle\`
2. Copy `kaggle.json` to that folder

## Step 3: Verify Setup

Run this command to test:
```bash
kaggle datasets list -s "credit card"