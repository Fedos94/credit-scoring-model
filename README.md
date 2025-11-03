Development and automation of a pipeline for a default prediction scoring model (PD-model)
==============================

Machine learning model for credit default prediction

Project Organization
------------

    credit_scoring_model/
├── LICENSE
├── Makefile                       <- Makefile with commands like `make data` or `make train`
├── README.md                      <- The top-level README for developers using this project.
├── .dockerignore
├── .env
├── .gitignore
├── DEPLOYMENT.md                  <- Deployment instructions
├── docker-compose.yml             <- Docker Compose configuration
├── Dockerfile                     <- Main Dockerfile for the application
├── Dockerfile.simple              <- Simplified Dockerfile
├── KAGGLE_SETUP.md                <- Kaggle API setup instructions
├── requirements.txt               <- The requirements file for reproducing the analysis environment
├── setup.py                       <- makes project pip installable (pip install -e .) so src can be imported
├── setup_kaggle.py                <- Kaggle setup script
├── test_environment.py            <- Environment testing script
├── tox.ini                        <- tox file with settings for running tox; see tox.readthedocs.io
│
├── data                           <- Data directory
│   ├── external                   <- Data from third party sources.
│   ├── interim                    <- Intermediate data that has been transformed.
│   ├── processed                  <- The final, canonical data sets for modeling.
│   └── raw                        <- The original, immutable data dump.
│
├── docs                           <- A default Sphinx project; see sphinx-doc.org for details
│   ├── Makefile
│   ├── commands.rst
│   ├── conf.py
│   ├── getting-started.rst
│   ├── index.rst
│   └── make.bat
│
├── models                         <- Trained and serialized models, model predictions, or model summaries
│   └── .gitkeep
│
├── notebooks                      <- Jupyter notebooks. Naming convention is a number (for ordering),
│   └── .gitkeep                   <- the creator's initials, and a short `-` delimited description
│
├── references                     <- Data dictionaries, manuals, and all other explanatory materials.
│   └── .gitkeep
│
├── reports                        <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures                    <- Generated graphics and figures to be used in reporting
│       └── .gitkeep
│
├── scripts                        <- Utility scripts for build, run, and management
│   ├── build.bat
│   ├── logs.bat
│   ├── reset.bat
│   ├── run.bat
│   ├── run_fixed.bat
│   ├── setup_kaggle.bat
│   ├── start_docker.bat
│   ├── status.bat
│   ├── stop.bat
│   └── test_kaggle.bat
│
└── src                            <- Source code for use in this project.
    ├── __init__.py                <- Makes src a Python module
    │
    ├── api                        <- API related code
    │   ├── __init__.py
    │   └── app.py                 <- FastAPI application
    │
    ├── data                       <- Scripts to download or generate data
    │   ├── __init__.py
    │   └── make_dataset.py
    │
    ├── features                   <- Scripts to turn raw data into features for modeling
    │   ├── __init__.py
    │   ├── .gitkeep
    │   └── build_features.py
    │
    ├── models                     <- Scripts to train models and then use trained models to make predictions
    │   ├── __init__.py
    │   ├── .gitkeep
    │   ├── predict_model.py
    │   └── train_model.py
    │
    ├── monitoring                 <- Monitoring and drift detection
    │   ├── __init__ .py
    │   └── drift_monitor.py
    │
    └── visualization              <- Scripts to create exploratory and results oriented visualizations
        ├── __init__.py
        ├── .gitkeep
        └── visualize.py

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

## Kaggle Dataset Setup

This project uses the "Default of Credit Card Clients Dataset" from Kaggle. 

### Option 1: Using kagglehub (Recommended)
The code automatically downloads the dataset using `kagglehub` - no authentication needed for public datasets:

```bash
pip install kagglehub
python src/data/make_dataset.py
# credit-scoring-model
Machine Learning API for credit scoring prediction
