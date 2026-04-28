"""
Machine Learning Models Training
Trains Random Forest, Linear Regression, and Logistic Regression models using the Iris dataset
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, mean_squared_error, r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class MLModelsTrainer:
    """Train and evaluate multiple ML models"""
    
    def __init__(self, dataset_path):
        """Initialize with dataset path"""
        self.dataset_path = Path(dataset_path)
        self.base_dir = Path(__file__).resolve().parent
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
        
    def load_data(self):
        """Load and explore the iris dataset"""
        print("=" * 70)
        print("LOADING DATA")
        print("=" * 70)

        if not self.dataset_path.exists():
            fallback_path = self.base_dir.parent / "15-04-26" / "data" / "iris.csv"
            if fallback_path.exists():
                self.dataset_path = fallback_path

        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        
        columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
        self.df = pd.read_csv(self.dataset_path, header=None, names=columns)
        
        print(f"\nDataset shape: {self.df.shape}")
        print(f"\nFirst few rows:\n{self.df.head()}")
        print("\nDataset info:")
        self.df.info()
        print(f"\nBasic statistics:\n{self.df.describe()}")
        print(f"\nClass distribution:\n{self.df['species'].value_counts()}")
        
    def preprocess_data(self):
        """Split and scale the data"""
        print("\n" + "=" * 70)
        print("DATA PREPROCESSING")
        print("=" * 70)
        
        species_mapping = {species: idx for idx, species in enumerate(sorted(self.df['species'].unique()))}
        print(f"\nSpecies mapping: {species_mapping}")
        
        X = self.df.drop('species', axis=1)
        y = self.df['species'].map(species_mapping)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTraining set size: {self.X_train.shape[0]}")
        print(f"Testing set size: {self.X_test.shape[0]}")
        
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        print("\nFeatures scaled using StandardScaler")
        
    def train_random_forest(self):
        """Train Random Forest Classifier"""
        print("\n" + "=" * 70)
        print("TRAINING RANDOM FOREST CLASSIFIER")
        print("=" * 70)
        
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(self.X_train, self.y_train)
        
        self.models['Random Forest'] = rf_model
        
        y_pred = rf_model.predict(self.X_test)
        
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted')
        recall = recall_score(self.y_test, y_pred, average='weighted')
        f1 = f1_score(self.y_test, y_pred, average='weighted')
        
        print(f"\nAccuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        print(f"\nConfusion Matrix:\n{confusion_matrix(self.y_test, y_pred)}")
        print(f"\nClassification Report:\n{classification_report(self.y_test, y_pred)}")
        
        feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        importances = rf_model.feature_importances_
        print(f"\nFeature Importances:")
        for name, importance in zip(feature_names, importances):
            print(f"  {name}: {importance:.4f}")
        
        self.results['Random Forest'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'y_pred': y_pred
        }
        
    def train_logistic_regression(self):
        """Train Logistic Regression Classifier"""
        print("\n" + "=" * 70)
        print("TRAINING LOGISTIC REGRESSION")
        print("=" * 70)
        
        lr_model = LogisticRegression(max_iter=1000, random_state=42)
        lr_model.fit(self.X_train, self.y_train)
        
        self.models['Logistic Regression'] = lr_model
        
        y_pred = lr_model.predict(self.X_test)
        
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted')
        recall = recall_score(self.y_test, y_pred, average='weighted')
        f1 = f1_score(self.y_test, y_pred, average='weighted')
        
        print(f"\nAccuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        print(f"\nConfusion Matrix:\n{confusion_matrix(self.y_test, y_pred)}")
        print(f"\nClassification Report:\n{classification_report(self.y_test, y_pred)}")
        
        self.results['Logistic Regression'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'y_pred': y_pred
        }
        
    def train_linear_regression(self):
        """Train Linear Regression model"""
        print("\n" + "=" * 70)
        print("TRAINING LINEAR REGRESSION")
        print("=" * 70)
        
        X_train_lr = self.X_train[:, :3]
        X_test_lr = self.X_test[:, :3]
        y_train_lr = self.X_train[:, 3]
        y_test_lr = self.X_test[:, 3]
        
        lr_reg_model = LinearRegression()
        lr_reg_model.fit(X_train_lr, y_train_lr)
        
        self.models['Linear Regression'] = lr_reg_model
        
        y_pred = lr_reg_model.predict(X_test_lr)
        
        mse = mean_squared_error(y_test_lr, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test_lr, y_pred)
        
        print(f"\nPredicting 'petal_width' from other features")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Root Mean Squared Error: {rmse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        print(f"\nCoefficients:")
        feature_names = ['sepal_length', 'sepal_width', 'petal_length']
        for name, coef in zip(feature_names, lr_reg_model.coef_):
            print(f"  {name}: {coef:.4f}")
        print(f"Intercept: {lr_reg_model.intercept_:.4f}")
        
        self.results['Linear Regression'] = {
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2,
            'y_pred': y_pred,
            'y_actual': y_test_lr
        }
        
    def compare_models(self):
        """Compare classifier models"""
        print("\n" + "=" * 70)
        print("MODEL COMPARISON")
        print("=" * 70)
        
        comparison_df = pd.DataFrame({
            model_name: metrics 
            for model_name, metrics in self.results.items() 
            if model_name != 'Linear Regression'
        }).T
        
        print("\nClassification Models Comparison:")
        print(comparison_df[['accuracy', 'precision', 'recall', 'f1_score']])
        
    def visualize_results(self):
        """Create visualizations of model results"""
        print("\n" + "=" * 70)
        print("GENERATING VISUALIZATIONS")
        print("=" * 70)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        models = ['Random Forest', 'Logistic Regression']
        accuracies = [self.results[m]['accuracy'] for m in models]
        axes[0, 0].bar(models, accuracies, color=['#2ecc71', '#3498db'])
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].set_title('Model Accuracy Comparison')
        axes[0, 0].set_ylim([0.9, 1.0])
        for i, v in enumerate(accuracies):
            axes[0, 0].text(i, v + 0.002, f'{v:.4f}', ha='center')
        
        f1_scores = [self.results[m]['f1_score'] for m in models]
        axes[0, 1].bar(models, f1_scores, color=['#2ecc71', '#3498db'])
        axes[0, 1].set_ylabel('F1-Score')
        axes[0, 1].set_title('Model F1-Score Comparison')
        axes[0, 1].set_ylim([0.9, 1.0])
        for i, v in enumerate(f1_scores):
            axes[0, 1].text(i, v + 0.002, f'{v:.4f}', ha='center')
        
        rf_metrics = self.results['Random Forest']
        metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        metrics_values = [rf_metrics['accuracy'], rf_metrics['precision'], 
                         rf_metrics['recall'], rf_metrics['f1_score']]
        axes[1, 0].bar(metrics_names, metrics_values, color='#2ecc71')
        axes[1, 0].set_ylabel('Score')
        axes[1, 0].set_title('Random Forest - All Metrics')
        axes[1, 0].set_ylim([0.9, 1.05])
        for i, v in enumerate(metrics_values):
            axes[1, 0].text(i, v + 0.01, f'{v:.4f}', ha='center')
        
        lr_metrics = self.results['Linear Regression']
        lr_metrics_names = ['MSE', 'RMSE', 'R² Score']
        lr_metrics_values = [lr_metrics['mse'], lr_metrics['rmse'], lr_metrics['r2_score']]
        axes[1, 1].bar(lr_metrics_names, lr_metrics_values, color='#e74c3c')
        axes[1, 1].set_ylabel('Score')
        axes[1, 1].set_title('Linear Regression - Metrics')
        for i, v in enumerate(lr_metrics_values):
            axes[1, 1].text(i, v + 0.01, f'{v:.4f}', ha='center')
        
        plt.tight_layout()
        output_path = self.base_dir / 'ml_models_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved as '{output_path.name}'")
        plt.show()
        
    def run_all(self):
        """Run complete training pipeline"""
        self.load_data()
        self.preprocess_data()
        self.train_random_forest()
        self.train_logistic_regression()
        self.train_linear_regression()
        self.compare_models()
        self.visualize_results()
        
        print("\n" + "=" * 70)
        print("TRAINING COMPLETE")
        print("=" * 70)


if __name__ == "__main__":
    dataset_path = Path(__file__).resolve().parent.parent / '15-04-26' / 'data' / 'iris.csv'
    trainer = MLModelsTrainer(dataset_path)
    trainer.run_all()
