import time
import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, Tuple
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score, f1_score
from core.jobs.progress import update_job_progress

logger = logging.getLogger(__name__)

class AdaptiveAutoMLEngine:
    """
    Intelligently scales model hyperparameter searching strategies dynamically 
    based on the underlying data footprint.
    """
    
    def __init__(self):
        # Thresholds
        self.SMALL_DATASET_THRESHOLD = 5000     # Rows < 5000 -> Grid Search
        self.MEDIUM_DATASET_THRESHOLD = 50000   # Rows < 50000 -> Random Search
        self.LARGE_SAMPLE_SIZE = 25000          # Rows > 50000 -> Sample this many for tuning
        
    def _get_regression_models(self):
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.linear_model import LinearRegression
        
        return {
            "Random Forest Regressor": {
                "estimator": RandomForestRegressor(random_state=42),
                "param_grid": {
                    "n_estimators": [50, 100],
                    "max_depth": [None, 10, 20],
                    "min_samples_split": [2, 5]
                }
            },
            "Gradient Boosting Regressor": {
                "estimator": GradientBoostingRegressor(random_state=42),
                "param_grid": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.01, 0.1],
                    "max_depth": [3, 5]
                }
            },
            "Linear Regression": {
                "estimator": LinearRegression(),
                "param_grid": {
                    "fit_intercept": [True, False]
                }
            }
        }
        
    def _get_classification_models(self):
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.linear_model import LogisticRegression
        
        return {
            "Random Forest Classifier": {
                "estimator": RandomForestClassifier(random_state=42),
                "param_grid": {
                    "n_estimators": [50, 100],
                    "max_depth": [None, 10],
                    "min_samples_split": [2, 5]
                }
            },
            "Gradient Boosting Classifier": {
                "estimator": GradientBoostingClassifier(random_state=42),
                "param_grid": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.01, 0.1],
                    "max_depth": [3, 5]
                }
            },
            "Logistic Regression": {
                "estimator": LogisticRegression(max_iter=1000),
                "param_grid": {
                    "C": [0.1, 1.0, 10.0]
                }
            }
        }
        
    def train(self, X: pd.DataFrame, y: pd.Series, task_type: str = "Regression") -> Tuple[list, Any, str, float]:
        """
        Executes adaptive hyperparameter tuning.
        Returns: (leaderboard, best_model_obj, best_model_name, best_metric_score)
        """
        num_rows = len(X)
        models_config = self._get_regression_models() if task_type == "Regression" else self._get_classification_models()
        
        # 1. Determine Search Strategy
        if num_rows <= self.SMALL_DATASET_THRESHOLD:
            strategy = "grid"
            update_job_progress(15, f"Small Dataset ({num_rows} rows). Strategy: Full Grid Search.")
            X_tune, y_tune = X, y
            
        elif num_rows <= self.MEDIUM_DATASET_THRESHOLD:
            strategy = "random"
            update_job_progress(15, f"Medium Dataset ({num_rows} rows). Strategy: Randomized Search.")
            X_tune, y_tune = X, y
            
        else:
            strategy = "random_sample"
            update_job_progress(15, f"Large Dataset ({num_rows} rows). Strategy: Sampling {self.LARGE_SAMPLE_SIZE} rows for tuning, retraining on full data.")
            # Sample for tuning only to save time
            X_tune = X.sample(n=self.LARGE_SAMPLE_SIZE, random_state=42)
            y_tune = y.loc[X_tune.index]

        # Standard train test split for final evaluation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        leaderboard = []
        best_metric = -float('inf')
        best_model_name = ""
        best_model_obj = None
        
        total_models = len(models_config)
        
        for idx, (name, config) in enumerate(models_config.items()):
            progress_base = 20 + int((idx / total_models) * 60)
            update_job_progress(progress_base, f"Tuning {name}...")
            start_time = time.time()
            
            # 2. Hyperparameter Tuning
            if strategy == "grid":
                search = GridSearchCV(config["estimator"], config["param_grid"], cv=3, n_jobs=-1)
                search.fit(X_tune, y_tune)
            else:
                search = RandomizedSearchCV(config["estimator"], config["param_grid"], n_iter=5, cv=3, random_state=42, n_jobs=-1)
                search.fit(X_tune, y_tune)
                
            best_params = search.best_params_
            best_estimator = search.best_estimator_
            
            update_job_progress(progress_base + 5, f"Retraining {name} with optimal parameters...")
            
            # 3. Retrain on Full Training Set (Crucial for large dataset sampling strategy)
            best_estimator.fit(X_train, y_train)
            
            # 4. Evaluate
            preds = best_estimator.predict(X_test)
            
            if task_type == "Regression":
                metric_score = r2_score(y_test, preds)
                run_metrics = {
                    "r2_score": round(metric_score, 4),
                    "rmse": round(np.sqrt(mean_squared_error(y_test, preds)), 4),
                    "mae": round(mean_absolute_error(y_test, preds), 4)
                }
            else:
                metric_score = accuracy_score(y_test, preds)
                run_metrics = {
                    "accuracy": round(metric_score, 4),
                    "f1_score": round(f1_score(y_test, preds, average='weighted'), 4)
                }
                
            # 5. Extract Importances
            importances = {}
            if hasattr(best_estimator, "feature_importances_"):
                importances = {list(X.columns)[i]: float(best_estimator.feature_importances_[i]) for i in range(len(X.columns))}
            elif hasattr(best_estimator, "coef_"):
                # Handle binary vs multiclass coef_ shapes safely
                coefs = best_estimator.coef_
                if len(coefs.shape) > 1 and coefs.shape[0] > 1:
                    coefs = np.mean(np.abs(coefs), axis=0) # Average over classes for simplicity
                else:
                    coefs = coefs[0]
                importances = {list(X.columns)[i]: float(abs(coefs[i])) for i in range(len(X.columns))}
                
            leaderboard.append({
                "model": name,
                "hyperparameters": best_params,
                "feature_importances": importances,
                "metrics": run_metrics,
                "primary_score": metric_score,
                "duration_secs": round(time.time() - start_time, 2)
            })
            
            if metric_score > best_metric:
                best_metric = metric_score
                best_model_name = name
                best_model_obj = best_estimator
                
        # Sort Leaderboard
        leaderboard = sorted(leaderboard, key=lambda x: x["primary_score"], reverse=True)
        return leaderboard, best_model_obj, best_model_name, best_metric

adaptive_automl = AdaptiveAutoMLEngine()
