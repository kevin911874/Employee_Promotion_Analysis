import joblib
import pandas as pd
import numpy as np
from typing import Dict, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import logging

logger = logging.getLogger(__name__)


class MLPredictionService:
    def __init__(self):
        self.model: RandomForestClassifier = None
        self.scaler: StandardScaler = None
        self.feature_names: List[str] = None
        self.categorical_mappings: Dict = {}
        
    def train_model(self, df: pd.DataFrame):
        """Train the Random Forest model with the data"""
        try:
            # Separate features and target
            X = df.drop(['employee_id', 'is_promoted'], axis=1)
            y = df['is_promoted']
            
            # Handle missing values
            X['previous_year_rating'].fillna(X['previous_year_rating'].median(), inplace=True)
            X['education'].fillna(X['education'].mode()[0], inplace=True)
            
            # Encode categorical variables
            categorical_cols = ['department', 'region', 'education', 'gender', 'recruitment_channel']
            X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
            
            self.feature_names = X_encoded.columns.tolist()
            
            # Scale features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X_encoded)
            
            # Handle imbalanced data with SMOTE
            smote = SMOTE(random_state=42, sampling_strategy=1.0)
            X_resampled, y_resampled = smote.fit_resample(X_scaled, y)
            
            # Train Random Forest
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_resampled, y_resampled)
            
            logger.info("Model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def save_model(self, model_path: str, scaler_path: str):
        """Save the trained model and scaler"""
        try:
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            joblib.dump(self.feature_names, model_path.replace('.joblib', '_features.joblib'))
            logger.info(f"Model saved to {model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    def load_model(self, model_path: str, scaler_path: str):
        """Load a trained model and scaler"""
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.feature_names = joblib.load(model_path.replace('.joblib', '_features.joblib'))
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_input(self, employee_data: Dict) -> np.ndarray:
        """Preprocess employee data for prediction"""
        try:
            # Create DataFrame
            df = pd.DataFrame([employee_data])
            
            # Handle missing values
            if 'previous_year_rating' not in df.columns or pd.isna(df['previous_year_rating'].iloc[0]):
                df['previous_year_rating'] = 3.0  # median value
            
            # Remove employee_id if present
            if 'employee_id' in df.columns:
                df = df.drop(['employee_id'], axis=1)
            
            # Encode categorical variables
            categorical_cols = ['department', 'region', 'education', 'gender', 'recruitment_channel']
            df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
            
            # Align with training features
            for col in self.feature_names:
                if col not in df_encoded.columns:
                    df_encoded[col] = 0
            
            df_encoded = df_encoded[self.feature_names]
            
            # Scale features
            X_scaled = self.scaler.transform(df_encoded)
            
            return X_scaled
            
        except Exception as e:
            logger.error(f"Error preprocessing input: {e}")
            raise
    
    def predict(self, employee_data: Dict) -> Dict:
        """Make promotion prediction for an employee"""
        try:
            X = self.preprocess_input(employee_data)
            
            # Get prediction and probability
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0]
            
            result = {
                "predicted_promotion": int(prediction),
                "promotion_probability": float(probability[1]),
                "no_promotion_probability": float(probability[0]),
                "confidence": float(max(probability))
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
    
    def predict_batch(self, employees_data: List[Dict]) -> List[Dict]:
        """Make predictions for multiple employees"""
        results = []
        for emp_data in employees_data:
            try:
                result = self.predict(emp_data)
                result['employee_id'] = emp_data.get('employee_id')
                results.append(result)
            except Exception as e:
                logger.error(f"Error predicting for employee {emp_data.get('employee_id')}: {e}")
                results.append({
                    'employee_id': emp_data.get('employee_id'),
                    'error': str(e)
                })
        return results
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance from the model"""
        try:
            if self.model is None:
                raise ValueError("Model not trained or loaded")
            
            importances = self.model.feature_importances_
            feature_importance = dict(zip(self.feature_names, importances))
            
            # Sort by importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            return {
                "features": [f[0] for f in sorted_features[:10]],
                "importances": [float(f[1]) for f in sorted_features[:10]]
            }
            
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
            raise
    
    def sensitivity_analysis(self, base_employee: Dict, feature: str, 
                           increments: List[float]) -> List[Dict]:
        """Perform sensitivity analysis on a specific feature"""
        results = []
        
        for increment in increments:
            emp_data = base_employee.copy()
            
            # Apply increment
            if feature in emp_data:
                original_value = emp_data[feature]
                emp_data[feature] = original_value * (1 + increment)
                
                # Make prediction
                prediction = self.predict(emp_data)
                
                results.append({
                    'increment': increment,
                    'new_value': emp_data[feature],
                    'promotion_probability': prediction['promotion_probability']
                })
        
        return results


# Global instance
ml_service = MLPredictionService()
