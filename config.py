"""
Configuración del proyecto de predicción de fidelización
"""

import os
from pathlib import Path
from sklearn.neural_network import MLPClassifier

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
RESULTS_DIR = PROJECT_ROOT / "results"
MODELS_DIR = RESULTS_DIR / "models"
FIGURES_DIR = RESULTS_DIR / "figures"
REPORTS_DIR = RESULTS_DIR / "reports"

# Configuración de datos
ONLINE_RETAIL_URL = "https://archive.ics.uci.edu/dataset/352/online+retail"
ONLINE_RETAIL_FILE = "online_retail.xlsx"

# Configuración de Google Trends
GOOGLE_TRENDS_KEYWORDS = [
    'online shopping',
    'retail therapy', 
    'gift shopping',
    'home decor',
    'christmas shopping'
]

GOOGLE_TRENDS_GEO = 'GB'  # Reino Unido

# Configuración del modelo
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Criterios para definir cliente fidelizable
LOYALTY_CRITERIA = {
    'frequency_threshold': 3,
    'monetary_percentile': 0.25,
    'recency_percentile': 0.75
}

# Configuración de segmentación
LOYALTY_SEGMENTS = {
    'high_potential': 0.8,
    'moderate_potential': 0.6,
    'low_potential': 0.4,
    'at_risk': 0.0
}

# Configuración de visualización
FIGURE_SIZE = (12, 8)
DPI = 300
STYLE = 'seaborn-v0_8'

# Configuración de modelos a evaluar
MODELS_CONFIG = {
    'logistic_regression': {
        'max_iter': 1000,
        'random_state': RANDOM_STATE
    },
    'random_forest': {
        'n_estimators': 100,
        'random_state': RANDOM_STATE
    },
    'gradient_boosting': {
        'n_estimators': 100,
        'random_state': RANDOM_STATE
    },
    'svm': {
        'probability': True,
        'random_state': RANDOM_STATE
    },
    'mlp_classifier': {
        'hidden_layer_sizes': (50, 25),
        'max_iter': 500,
        'random_state': RANDOM_STATE,
        'early_stopping': True,
        'validation_fraction': 0.2,
        'alpha': 0.01,  # Más regularización L2
        'learning_rate_init': 0.001
    },
    'deep_neural_network': {
        'layers': [64, 32],
        'dropout_rate': 0.5,
        'epochs': 50,
        'batch_size': 32,
        'learning_rate': 0.001
    }
}

# Grids de hiperparámetros para optimización
PARAM_GRIDS = {
    'random_forest': {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    },
    'gradient_boosting': {
        'n_estimators': [100, 200],
        'learning_rate': [0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7]
    },
    'logistic_regression': {
        'C': [0.1, 1.0, 10.0],
        'penalty': ['l1', 'l2']
    },
    'mlp_classifier': {
        'hidden_layer_sizes': [(100,), (100, 50), (128, 64)],
        'learning_rate_init': [0.001, 0.01],
        'alpha': [0.0001, 0.001]
    },
    'deep_neural_network': {
        'layers': [[64, 32], [128, 64, 32], [256, 128, 64]],
        'dropout_rate': [0.2, 0.3, 0.4],
        'learning_rate': [0.001, 0.01]
    }
}

# Métricas de evaluación
EVALUATION_METRICS = [
    'accuracy',
    'precision',
    'recall',
    'f1',
    'roc_auc'
]

# Configuración para Tableau
TABLEAU_EXPORT_COLUMNS = [
    'CustomerID',
    'Recency',
    'Frequency', 
    'Monetary',
    'UniqueProducts',
    'Country',
    'Loyalty_Prediction',
    'Loyalty_Probability',
    'Loyalty_Segment'
]
