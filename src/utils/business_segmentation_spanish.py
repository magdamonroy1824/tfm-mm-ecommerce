"""
Segmentación de clientes y recomendaciones de negocio en español
TFM: Predicción de Fidelización - Magda Monroy Jiménez
"""

import pandas as pd
import numpy as np

def get_customer_segment(recency, frequency, monetary, probability):
    """
    Segmentación RFM + Probabilidad con paleta original que funcionaba bien
    """
    
    # Segmentación RFM con colores originales consistentes
    if recency <= 30 and frequency >= 8 and monetary >= 1000:
        if probability >= 0.8:
            return "Campeones", "🏆", "#28a745"  # Verde success
        else:
            return "Clientes Leales", "💎", "#17a2b8"  # Azul info
    
    elif recency <= 60 and frequency >= 5 and monetary >= 500:
        if probability >= 0.7:
            return "Potenciales Leales", "⭐", "#ffc107"  # Amarillo warning
        else:
            return "Nuevos Clientes", "🌱", "#6f42c1"  # Púrpura
    
    elif recency <= 90 and frequency >= 3:
        if probability >= 0.6:
            return "Prometedores", "📈", "#fd7e14"  # Naranja
        else:
            return "Necesitan Atención", "⚠️", "#dc3545"  # Rojo danger
    
    elif recency > 90 and frequency >= 2:
        return "En Riesgo", "🚨", "#e83e8c"  # Rosa
    
    else:
        return "Perdidos", "💔", "#6c757d"  # Gris secondary

def get_business_recommendations(segment, recency, frequency, monetary, probability):
    """
    Recomendaciones específicas de negocio por segmento
    """
    
    recommendations = {
        "Campeones": {
            "strategy": "Recompensar y Retener",
            "actions": [
                "🎁 Programa VIP exclusivo",
                "💰 Descuentos por volumen (15-20%)",
                "🚀 Acceso anticipado a nuevos productos",
                "📞 Atención personalizada premium"
            ],
            "budget": "Alto",
            "priority": "Máxima",
            "roi_expected": "300-500%"
        },
        
        "Clientes Leales": {
            "strategy": "Nutrir y Venta Cruzada",
            "actions": [
                "🛍️ Venta cruzada personalizada",
                "💳 Programa de puntos premium",
                "📧 Newsletter exclusivo",
                "🎯 Ofertas en categorías favoritas"
            ],
            "budget": "Alto",
            "priority": "Alta",
            "roi_expected": "200-300%"
        },
        
        "Potenciales Leales": {
            "strategy": "Desarrollar y Convertir",
            "actions": [
                "📱 Incorporación personalizada",
                "🎁 Descuento en segunda compra (10%)",
                "📊 Recomendaciones basadas en historial",
                "⏰ Recordatorios de recompra"
            ],
            "budget": "Medio",
            "priority": "Alta",
            "roi_expected": "150-250%"
        },
        
        "Nuevos Clientes": {
            "strategy": "Educar y Comprometer",
            "actions": [
                "👋 Serie de bienvenida (3 emails)",
                "🎁 Descuento de bienvenida (5-10%)",
                "📚 Guías de producto",
                "💬 Encuesta de satisfacción"
            ],
            "budget": "Medio",
            "priority": "Media",
            "roi_expected": "100-150%"
        },
        
        "Prometedores": {
            "strategy": "Activar y Motivar",
            "actions": [
                "🔥 Ofertas limitadas en tiempo",
                "📦 Envío gratuito en próxima compra",
                "🎯 Retargeting personalizado",
                "📞 Llamada de seguimiento"
            ],
            "budget": "Medio",
            "priority": "Media",
            "roi_expected": "80-120%"
        },
        
        "Necesitan Atención": {
            "strategy": "Re-comprometer y Recuperar",
            "actions": [
                "💌 Campaña de reactivación",
                "🎁 Oferta especial (15-25%)",
                "📋 Encuesta de retroalimentación",
                "🆕 Mostrar nuevos productos"
            ],
            "budget": "Bajo-Medio",
            "priority": "Media",
            "roi_expected": "50-100%"
        },
        
        "En Riesgo": {
            "strategy": "Recuperar Urgentemente",
            "actions": [
                "🚨 Campaña urgente de retención",
                "💥 Descuento agresivo (20-30%)",
                "📞 Contacto directo del equipo",
                "🎁 Regalo sorpresa"
            ],
            "budget": "Bajo",
            "priority": "Baja",
            "roi_expected": "20-50%"
        },
        
        "Perdidos": {
            "strategy": "Última Oportunidad de Recuperación",
            "actions": [
                "💔 Campaña de despedida",
                "🎁 Oferta final irresistible (30-40%)",
                "📊 Análisis de por qué se perdió",
                "🔄 Remarketing a largo plazo"
            ],
            "budget": "Muy Bajo",
            "priority": "Muy Baja",
            "roi_expected": "0-20%"
        }
    }
    
    return recommendations.get(segment, recommendations["Perdidos"])

def calculate_customer_value_score(recency, frequency, monetary, probability):
    """
    Calcular puntuación de valor del cliente (0-100)
    """
    # Normalizar métricas (0-1)
    recency_score = max(0, (365 - recency) / 365)  # Más reciente = mejor
    frequency_score = min(1, frequency / 20)  # Normalizar a máximo 20 compras
    monetary_score = min(1, monetary / 5000)  # Normalizar a máximo £5000
    
    # Pesos: Probabilidad 40%, Monetario 30%, Frecuencia 20%, Recencia 10%
    total_score = (
        probability * 0.4 +
        monetary_score * 0.3 +
        frequency_score * 0.2 +
        recency_score * 0.1
    ) * 100
    
    return round(total_score, 1)

def get_campaign_budget_allocation(segment, customer_value_score):
    """
    Sugerir presupuesto de campaña por cliente
    """
    base_budgets = {
        "Campeones": 50,
        "Clientes Leales": 35,
        "Potenciales Leales": 25,
        "Nuevos Clientes": 15,
        "Prometedores": 20,
        "Necesitan Atención": 12,
        "En Riesgo": 8,
        "Perdidos": 3
    }
    
    base = base_budgets.get(segment, 5)
    
    # Ajustar por valor del cliente
    if customer_value_score >= 80:
        multiplier = 1.5
    elif customer_value_score >= 60:
        multiplier = 1.2
    elif customer_value_score >= 40:
        multiplier = 1.0
    else:
        multiplier = 0.7
    
    return round(base * multiplier, 2)

def generate_customer_insights(customer_data):
    """
    Generar insights completos para un cliente
    """
    recency = customer_data['Recency']
    frequency = customer_data['Frequency'] 
    monetary = customer_data['Monetary']
    probability = customer_data.get('probability', 0.5)
    
    # Segmentación
    segment, icon, color = get_customer_segment(recency, frequency, monetary, probability)
    
    # Recomendaciones
    recommendations = get_business_recommendations(segment, recency, frequency, monetary, probability)
    
    # Métricas adicionales
    value_score = calculate_customer_value_score(recency, frequency, monetary, probability)
    suggested_budget = get_campaign_budget_allocation(segment, value_score)
    
    # Análisis de riesgo
    if recency > 180:
        risk_level = "Alto"
        risk_color = "#dc3545"
    elif recency > 90:
        risk_level = "Medio"
        risk_color = "#ffc107"
    else:
        risk_level = "Bajo"
        risk_color = "#28a745"
    
    return {
        "segment": segment,
        "segment_icon": icon,
        "segment_color": color,
        "probability": probability,
        "value_score": value_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "recommendations": recommendations,
        "suggested_budget": suggested_budget,
        "next_actions": recommendations["actions"][:2],  # Top 2 acciones
        "campaign_priority": recommendations["priority"],
        "expected_roi": recommendations["roi_expected"]
    }
