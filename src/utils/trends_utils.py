"""
Utilidades para integración con Google Trends
"""

import pandas as pd
import numpy as np
from pytrends.request import TrendReq
import time
from datetime import datetime


def get_google_trends_data(keywords, timeframe, geo='GB', retries=3):
    """
    Obtiene datos de Google Trends para una lista de palabras clave
    
    Args:
        keywords (list): Lista de términos de búsqueda
        timeframe (str): Período de tiempo (formato: 'YYYY-MM-DD YYYY-MM-DD')
        geo (str): Código de país (default: 'GB' para Reino Unido)
        retries (int): Número de reintentos en caso de error
        
    Returns:
        pd.DataFrame: Datos de tendencias con fechas como índice
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    trends_data = pd.DataFrame()
    
    for keyword in keywords:
        success = False
        attempts = 0
        
        while not success and attempts < retries:
            try:
                # Configurar búsqueda
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
                
                # Obtener datos de interés a lo largo del tiempo
                interest_over_time = pytrends.interest_over_time()
                
                if not interest_over_time.empty:
                    # Limpiar y renombrar
                    interest_over_time = interest_over_time.drop('isPartial', axis=1, errors='ignore')
                    interest_over_time.columns = [f'trends_{keyword.replace(" ", "_")}']
                    
                    if trends_data.empty:
                        trends_data = interest_over_time
                    else:
                        trends_data = trends_data.join(interest_over_time, how='outer')
                
                success = True
                print(f"Datos obtenidos para '{keyword}'")
                
            except Exception as e:
                attempts += 1
                print(f"Error obteniendo datos para '{keyword}' (intento {attempts}): {e}")
                if attempts < retries:
                    time.sleep(5)  # Esperar antes de reintentar
            
            # Pausa para evitar límites de API
            time.sleep(2)
    
    return trends_data


def aggregate_trends_monthly(trends_data):
    """
    Agrega datos de tendencias por mes
    
    Args:
        trends_data (pd.DataFrame): Datos de tendencias con fechas como índice
        
    Returns:
        pd.DataFrame: Datos agregados por mes
    """
    if trends_data.empty:
        return pd.DataFrame()
    
    trends_monthly = trends_data.reset_index()
    trends_monthly['date'] = pd.to_datetime(trends_monthly['date'])
    trends_monthly['year_month'] = trends_monthly['date'].dt.to_period('M')
    
    # Agregar por mes
    trends_monthly_agg = trends_monthly.groupby('year_month').mean().reset_index()
    trends_monthly_agg['year_month'] = trends_monthly_agg['year_month'].astype(str)
    
    return trends_monthly_agg


def create_synthetic_trends_data(start_date, end_date, keywords):
    """
    Crea datos sintéticos de tendencias para demostración
    
    Args:
        start_date (str): Fecha de inicio (YYYY-MM-DD)
        end_date (str): Fecha de fin (YYYY-MM-DD)
        keywords (list): Lista de términos de búsqueda
        
    Returns:
        pd.DataFrame: Datos sintéticos de tendencias
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq='W')
    
    trends_data = pd.DataFrame({'date': date_range})
    
    for keyword in keywords:
        col_name = f'trends_{keyword.replace(" ", "_")}'
        # Crear datos con cierta estacionalidad y ruido
        base_trend = 50 + 30 * np.sin(2 * np.pi * np.arange(len(date_range)) / 52)  # Ciclo anual
        noise = np.random.normal(0, 10, len(date_range))
        trends_data[col_name] = np.clip(base_trend + noise, 0, 100).astype(int)
    
    return trends_data


def merge_trends_with_customers(customer_data, trends_data, transaction_data):
    """
    Combina datos de tendencias con información de clientes
    
    Args:
        customer_data (pd.DataFrame): Datos de clientes
        trends_data (pd.DataFrame): Datos de tendencias agregados por mes
        transaction_data (pd.DataFrame): Datos de transacciones
        
    Returns:
        pd.DataFrame: Dataset combinado con características de tendencias
    """
    # Agregar año-mes a las transacciones
    transaction_data = transaction_data.copy()
    transaction_data['year_month'] = transaction_data['InvoiceDate'].dt.to_period('M').astype(str)
    
    # Calcular actividad por cliente y mes
    customer_monthly = transaction_data.groupby(['CustomerID', 'year_month']).agg({
        'Revenue': 'sum',
        'InvoiceNo': 'nunique',
        'Quantity': 'sum'
    }).reset_index()
    
    # Unir con datos de tendencias
    customer_trends = customer_monthly.merge(trends_data, on='year_month', how='left')
    
    # Agregar características de tendencias por cliente
    trends_columns = [col for col in trends_data.columns if col.startswith('trends_')]
    
    agg_dict = {}
    for col in trends_columns:
        agg_dict[col] = ['mean', 'std', 'max']
    
    customer_trends_features = customer_trends.groupby('CustomerID').agg(agg_dict).reset_index()
    
    # Aplanar nombres de columnas
    new_columns = ['CustomerID']
    for col in trends_columns:
        new_columns.extend([f'avg_{col}', f'std_{col}', f'max_{col}'])
    
    customer_trends_features.columns = new_columns
    
    # Combinar con datos de clientes
    final_dataset = customer_data.merge(customer_trends_features, on='CustomerID', how='left')
    
    # Rellenar valores faltantes con la media
    for col in new_columns[1:]:  # Excluir CustomerID
        if col in final_dataset.columns:
            final_dataset[col] = final_dataset[col].fillna(final_dataset[col].mean())
    
    return final_dataset


def analyze_trends_correlation(df, target_col='IsLoyal'):
    """
    Analiza la correlación entre tendencias y la variable objetivo
    
    Args:
        df (pd.DataFrame): Dataset con características de tendencias
        target_col (str): Nombre de la variable objetivo
        
    Returns:
        pd.Series: Correlaciones ordenadas por valor absoluto
    """
    trends_columns = [col for col in df.columns if 'trends' in col]
    
    if target_col in df.columns and trends_columns:
        correlations = df[trends_columns + [target_col]].corr()[target_col].drop(target_col)
        return correlations.sort_values(key=abs, ascending=False)
    else:
        return pd.Series()
