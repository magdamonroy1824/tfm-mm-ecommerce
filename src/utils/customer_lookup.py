"""
Funcionalidad de búsqueda de clientes reales
TFM: Predicción de Fidelización - Magda Monroy Jiménez
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_customer_database():
    """Cargar base de datos de clientes"""
    try:
        df = pd.read_csv('data/processed/customer_features_with_trends.csv')
        return df
    except FileNotFoundError:
        return None

def search_customer_by_id(customer_id):
    """Buscar cliente por ID"""
    df = load_customer_database()
    if df is None:
        return None
    
    # Buscar por CustomerID exacto o parcial
    if customer_id.isdigit():
        # Búsqueda por ID numérico
        customer = df[df['CustomerID'] == int(customer_id)]
    else:
        # Búsqueda por string (puede incluir CUST- prefix)
        numeric_id = ''.join(filter(str.isdigit, customer_id))
        if numeric_id:
            customer = df[df['CustomerID'] == int(numeric_id)]
        else:
            return None
    
    if len(customer) > 0:
        return customer.iloc[0].to_dict()
    return None

def get_random_customers(n=5):
    """Obtener clientes aleatorios para demo"""
    df = load_customer_database()
    if df is None:
        return []
    
    sample = df.sample(min(n, len(df)))
    customers = []
    
    for _, row in sample.iterrows():
        customers.append({
            'id': f"CUST-{row['CustomerID']}",
            'recency': int(row['Recency']),
            'frequency': int(row['Frequency']),
            'monetary': int(row['Monetary']),
            'unique_products': int(row['UniqueProducts']),
            'country': row.get('Country', 'Unknown')
        })
    
    return customers

def get_top_customers_by_value(n=10):
    """Obtener top clientes por valor monetario"""
    df = load_customer_database()
    if df is None:
        return []
    
    top_customers = df.nlargest(n, 'Monetary')
    customers = []
    
    for _, row in top_customers.iterrows():
        customers.append({
            'id': f"CUST-{row['CustomerID']}",
            'recency': int(row['Recency']),
            'frequency': int(row['Frequency']),
            'monetary': int(row['Monetary']),
            'unique_products': int(row['UniqueProducts']),
            'country': row.get('Country', 'Unknown'),
            'rank': len(customers) + 1
        })
    
    return customers

def get_customers_at_risk(n=10):
    """Obtener clientes en riesgo con alto valor histórico"""
    df = load_customer_database()
    if df is None:
        return []
    
    # Clientes con alta recencia pero buen valor histórico
    at_risk = df[
        (df['Recency'] > 90) & 
        (df['Monetary'] > df['Monetary'].median())
    ].nlargest(n, 'Monetary')
    
    customers = []
    for _, row in at_risk.iterrows():
        customers.append({
            'id': f"CUST-{row['CustomerID']}",
            'recency': int(row['Recency']),
            'frequency': int(row['Frequency']),
            'monetary': int(row['Monetary']),
            'unique_products': int(row['UniqueProducts']),
            'country': row.get('Country', 'Unknown'),
            'risk_score': row['Recency']  # Usar recency como score de riesgo
        })
    
    return customers

def format_customer_display(customer_data):
    """Formatear datos del cliente para mostrar"""
    if not customer_data:
        return "Customer not found"
    
    return f"""
    **Customer ID:** {customer_data.get('id', 'N/A')}
    **Recency:** {customer_data.get('recency', 0)} days
    **Frequency:** {customer_data.get('frequency', 0)} purchases  
    **Monetary:** £{customer_data.get('monetary', 0):,}
    **Products:** {customer_data.get('unique_products', 0)} unique items
    **Country:** {customer_data.get('country', 'Unknown')}
    """
