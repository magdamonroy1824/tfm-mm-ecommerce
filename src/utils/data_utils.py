"""
Utilidades para procesamiento de datos del proyecto de fidelización
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler, LabelEncoder


def load_and_clean_retail_data(file_path):
    """
    Carga y limpia el dataset Online Retail
    
    Args:
        file_path (str): Ruta al archivo Excel
        
    Returns:
        pd.DataFrame: Dataset limpio
    """
    # Cargar datos
    df = pd.read_excel(file_path)
    
    # Convertir fecha
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Limpieza básica
    df_clean = df.dropna(subset=['CustomerID'])
    df_clean = df_clean[~df_clean['InvoiceNo'].astype(str).str.startswith('C')]
    df_clean = df_clean[df_clean['Quantity'] > 0]
    df_clean = df_clean[df_clean['UnitPrice'] > 0]
    
    # Crear variable de ingresos
    df_clean['Revenue'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    return df_clean


def calculate_rfm_metrics(df, customer_col='CustomerID', date_col='InvoiceDate', 
                         revenue_col='Revenue', invoice_col='InvoiceNo'):
    """
    Calcula métricas RFM para cada cliente
    
    Args:
        df (pd.DataFrame): Dataset de transacciones
        customer_col (str): Nombre de la columna de cliente
        date_col (str): Nombre de la columna de fecha
        revenue_col (str): Nombre de la columna de ingresos
        invoice_col (str): Nombre de la columna de factura
        
    Returns:
        pd.DataFrame: Métricas RFM por cliente
    """
    reference_date = df[date_col].max() + timedelta(days=1)
    
    rfm = df.groupby(customer_col).agg({
        date_col: lambda x: (reference_date - x.max()).days,  # Recency
        invoice_col: 'nunique',  # Frequency
        revenue_col: 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = [customer_col, 'Recency', 'Frequency', 'Monetary']
    
    return rfm


def create_customer_features(df, customer_col='CustomerID'):
    """
    Crea características adicionales por cliente
    
    Args:
        df (pd.DataFrame): Dataset de transacciones
        customer_col (str): Nombre de la columna de cliente
        
    Returns:
        pd.DataFrame: Características por cliente
    """
    features = df.groupby(customer_col).agg({
        'Quantity': ['sum', 'mean', 'std'],
        'UnitPrice': ['mean', 'std'],
        'Revenue': ['sum', 'mean', 'std'],
        'StockCode': 'nunique',
        'InvoiceDate': ['min', 'max'],
        'Country': lambda x: x.mode()[0] if not x.empty else 'Unknown'
    }).reset_index()
    
    # Aplanar nombres de columnas
    features.columns = [customer_col, 'TotalQuantity', 'AvgQuantity', 'StdQuantity',
                       'AvgUnitPrice', 'StdUnitPrice', 'TotalRevenue', 'AvgRevenue', 
                       'StdRevenue', 'UniqueProducts', 'FirstPurchase', 'LastPurchase', 'Country']
    
    # Calcular duración como cliente
    features['CustomerLifespan'] = (features['LastPurchase'] - features['FirstPurchase']).dt.days
    
    return features


def define_loyalty_target(df, freq_threshold=3, monetary_percentile=0.25, recency_percentile=0.75):
    """
    Define la variable objetivo de fidelización
    
    Args:
        df (pd.DataFrame): Dataset con métricas RFM
        freq_threshold (int): Umbral mínimo de frecuencia
        monetary_percentile (float): Percentil mínimo de valor monetario
        recency_percentile (float): Percentil máximo de recencia
        
    Returns:
        pd.Series: Variable objetivo binaria
    """
    monetary_threshold = df['Monetary'].quantile(monetary_percentile)
    recency_threshold = df['Recency'].quantile(recency_percentile)
    
    is_loyal = (
        (df['Frequency'] >= freq_threshold) & 
        (df['Monetary'] >= monetary_threshold) & 
        (df['Recency'] <= recency_threshold)
    ).astype(int)
    
    return is_loyal


def prepare_features_for_modeling(df, categorical_cols=None):
    """
    Prepara características para modelado
    
    Args:
        df (pd.DataFrame): Dataset con características
        categorical_cols (list): Lista de columnas categóricas
        
    Returns:
        tuple: (X, feature_names, encoders)
    """
    df_model = df.copy()
    encoders = {}
    
    if categorical_cols:
        for col in categorical_cols:
            if col in df_model.columns:
                le = LabelEncoder()
                df_model[f'{col}_encoded'] = le.fit_transform(df_model[col].fillna('Unknown'))
                encoders[col] = le
    
    # Seleccionar columnas numéricas
    numeric_cols = df_model.select_dtypes(include=[np.number]).columns.tolist()
    
    # Excluir ID y target si están presentes
    exclude_cols = ['CustomerID', 'IsLoyal']
    feature_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    X = df_model[feature_cols].fillna(0)
    
    return X, feature_cols, encoders
