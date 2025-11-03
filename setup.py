from setuptools import setup, find_packages

setup(
    name="credit_scoring_model",
    version="0.1.0",
    description="ML pipeline for credit default prediction",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "scikit-learn>=1.0.0",
        "mlflow>=2.0.0",
        "dvc>=3.0.0",
    ],
)