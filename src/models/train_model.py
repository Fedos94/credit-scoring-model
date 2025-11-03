import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score, roc_curve
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import json
import os
from src.features.build_features import create_feature_pipeline

class ModelTrainer:
    def __init__(self, experiment_name="credit_scoring"):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)
        
    def load_data(self):
        """Load processed data"""
        train_df = pd.read_csv("data/processed/train.csv")
        test_df = pd.read_csv("data/processed/test.csv")
        
        X_train = train_df.drop('DEFAULT', axis=1)
        y_train = train_df['DEFAULT']
        X_test = test_df.drop('DEFAULT', axis=1)
        y_test = test_df['DEFAULT']
        
        return X_train, X_test, y_train, y_test
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred)
        }
        
        # Plot ROC curve
        os.makedirs('reports/figures', exist_ok=True)
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {model_name}')
        plt.legend(loc="lower right")
        plt.savefig(f'reports/figures/roc_curve_{model_name}.png')
        plt.close()
        
        return metrics
    
    def train_logistic_regression(self, X_train, y_train, X_test, y_test):
        """Train logistic regression model"""
        with mlflow.start_run(run_name="logistic_regression"):
            preprocessor = create_feature_pipeline(X_train)
            
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', LogisticRegression(random_state=42, max_iter=1000))
            ])
            
            param_grid = {
                'classifier__C': [0.1, 1, 10],
                'classifier__penalty': ['l1', 'l2'],
                'classifier__solver': ['liblinear']
            }
            
            grid_search = GridSearchCV(
                pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1
            )
            
            grid_search.fit(X_train, y_train)
            
            # Log parameters and metrics
            mlflow.log_params(grid_search.best_params_)
            mlflow.log_metric("best_cv_score", grid_search.best_score_)
            
            metrics = self.evaluate_model(grid_search.best_estimator_, X_test, y_test, "logistic_regression")
            
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log artifacts
            mlflow.log_artifact(f'reports/figures/roc_curve_logistic_regression.png')
            mlflow.sklearn.log_model(grid_search.best_estimator_, "model")
            
            return grid_search.best_estimator_, metrics
    
    def train_gradient_boosting(self, X_train, y_train, X_test, y_test):
        """Train gradient boosting model"""
        with mlflow.start_run(run_name="gradient_boosting"):
            preprocessor = create_feature_pipeline(X_train)
            
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', GradientBoostingClassifier(random_state=42))
            ])
            
            param_dist = {
                'classifier__n_estimators': [100, 200],
                'classifier__learning_rate': [0.01, 0.1],
                'classifier__max_depth': [3, 4],
                'classifier__min_samples_split': [2, 5]
            }
            
            random_search = RandomizedSearchCV(
                pipeline, param_dist, n_iter=4, cv=3, 
                scoring='roc_auc', random_state=42, n_jobs=-1
            )
            
            random_search.fit(X_train, y_train)
            
            # Log parameters and metrics
            mlflow.log_params(random_search.best_params_)
            mlflow.log_metric("best_cv_score", random_search.best_score_)
            
            metrics = self.evaluate_model(random_search.best_estimator_, X_test, y_test, "gradient_boosting")
            
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log artifacts
            mlflow.log_artifact(f'reports/figures/roc_curve_gradient_boosting.png')
            mlflow.sklearn.log_model(random_search.best_estimator_, "model")
            
            return random_search.best_estimator_, metrics
    
    def train(self):
        """Main training function"""
        X_train, X_test, y_train, y_test = self.load_data()
        
        # Ensure models directory exists
        os.makedirs('models', exist_ok=True)
        
        # Train multiple models
        print("Training Logistic Regression...")
        lr_model, lr_metrics = self.train_logistic_regression(X_train, y_train, X_test, y_test)
        
        print("Training Gradient Boosting...")
        gb_model, gb_metrics = self.train_gradient_boosting(X_train, y_train, X_test, y_test)
        
        # Compare models and select best
        if lr_metrics['roc_auc'] > gb_metrics['roc_auc']:
            best_model = lr_model
            best_metrics = lr_metrics
            best_model_name = "logistic_regression"
        else:
            best_model = gb_model
            best_metrics = gb_metrics
            best_model_name = "gradient_boosting"
        
        # Save best model
        joblib.dump(best_model, 'models/best_model.pkl')
        
        # Save metrics
        with open('models/metrics.json', 'w') as f:
            json.dump(best_metrics, f, indent=2)
        
        print(f"Best model: {best_model_name}")
        print(f"Best ROC-AUC: {best_metrics['roc_auc']:.4f}")
        
        return best_model, best_metrics

def train_model():
    """Convenience function for training model"""
    trainer = ModelTrainer()
    return trainer.train()

if __name__ == "__main__":
    train_model()