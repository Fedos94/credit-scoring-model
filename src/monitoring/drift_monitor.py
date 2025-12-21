import pandas as pd
import numpy as np
import requests
import json
from scipy.stats import ks_2samp
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.predict_model import load_model, predict_proba

def calculate_psi(expected, actual, buckets=10):
    """Calculate Population Stability Index"""
    # Create buckets based on expected distribution
    breakpoints = np.percentile(expected, [100/buckets * i for i in range(buckets+1)])
    
    expected_percents = np.histogram(expected, breakpoints)[0] / len(expected)
    actual_percents = np.histogram(actual, breakpoints)[0] / len(actual)
    
    # Avoid division by zero
    expected_percents = np.clip(expected_percents, 0.001, 1.0)
    actual_percents = np.clip(actual_percents, 0.001, 1.0)
    
    psi = np.sum((expected_percents - actual_percents) * np.log(expected_percents / actual_percents))
    return psi

class DriftMonitor:
    def __init__(self, api_url: str = None, train_data_path: str = None):
        self.api_url = api_url
        if train_data_path is None:
            train_data_path = "data/processed/train.csv"
        self.train_data = pd.read_csv(train_data_path)
        self.model = load_model()
    
    def get_train_predictions(self):
        """Get predictions on training data"""
        X_train = self.train_data.drop('DEFAULT', axis=1)
        return predict_proba(self.model, X_train)
    
    def simulate_production_data(self, n_samples: int = 100):
        """Simulate production data by sampling from test set"""
        test_data = pd.read_csv('data/processed/test.csv')
        return test_data.sample(n_samples, random_state=42)
    
    def get_api_predictions(self, data: pd.DataFrame) -> np.ndarray:
        """Get predictions from API"""
        if self.api_url is None:
            return predict_proba(self.model, data.drop('DEFAULT', axis=1))
        
        probabilities = []
        
        for _, row in data.iterrows():
            # Prepare request data
            request_data = row.drop('DEFAULT').to_dict()
            
            try:
                response = requests.post(
                    f"{self.api_url}/predict",
                    json=request_data,
                    timeout=10
                )
                if response.status_code == 200:
                    result = response.json()
                    probabilities.append(result['probability'])
                else:
                    probabilities.append(np.nan)
            except:
                probabilities.append(np.nan)
        
        return np.array(probabilities)
    
    def monitor_drift(self, n_samples: int = 100):
        """Monitor data and prediction drift"""
        # Get training predictions
        train_predictions = self.get_train_predictions()
        
        # Simulate new production data
        new_data = self.simulate_production_data(n_samples)
        new_predictions = self.get_api_predictions(new_data)
        
        # Remove NaN values
        mask = ~np.isnan(new_predictions)
        new_predictions = new_predictions[mask]
        new_data = new_data[mask]
        
        if len(new_predictions) == 0:
            return {"error": "No valid predictions received"}
        
        # Calculate PSI for predictions
        psi_score = calculate_psi(train_predictions[:len(new_predictions)], new_predictions)
        
        # Calculate KS test for key features
        drift_report = {
            'psi_score': float(psi_score),
            'feature_drift': {},
            'drift_detected': psi_score > 0.1
        }
        
        # Check key features for drift
        key_features = ['LIMIT_BAL', 'AGE', 'BILL_AMT1', 'PAY_0']
        
        for feature in key_features:
            if feature in self.train_data.columns and feature in new_data.columns:
                ks_stat, p_value = ks_2samp(
                    self.train_data[feature].sample(min(len(new_data), 1000), random_state=42),
                    new_data[feature]
                )
                drift_report['feature_drift'][feature] = {
                    'ks_statistic': float(ks_stat),
                    'p_value': float(p_value),
                    'drift_detected': p_value < 0.05
                }
        
        # Alert if significant drift detected
        if psi_score > 0.1:
            print(f"WARNING: Significant prediction drift detected! PSI: {psi_score:.4f}")
        
        return drift_report

if __name__ == "__main__":
    monitor = DriftMonitor("http://localhost:8000")
    report = monitor.monitor_drift()
    print("Drift Monitoring Report:")
    print(json.dumps(report, indent=2))