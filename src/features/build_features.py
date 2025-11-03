import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

def create_feature_pipeline(X_train):
    """Create feature preprocessing pipeline"""
    
    # Identify numeric and categorical columns
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Remove target variable if present
    if 'DEFAULT' in numeric_features:
        numeric_features.remove('DEFAULT')
    
    # Numeric transformer
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    return preprocessor

def get_feature_names(preprocessor, X_train):
    """Get feature names after preprocessing"""
    feature_names = []
    
    # Numeric features
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if 'DEFAULT' in numeric_features:
        numeric_features.remove('DEFAULT')
    feature_names.extend(numeric_features)
    
    # Categorical features
    categorical_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    for col in categorical_features:
        # Get unique values for each categorical column
        unique_vals = X_train[col].unique()
        feature_names.extend([f"{col}_{val}" for val in sorted(unique_vals)])
    
    return feature_names