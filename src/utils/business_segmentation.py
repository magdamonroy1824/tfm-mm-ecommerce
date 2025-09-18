"""
Segmentación de clientes y recomendaciones de negocio
TFM: Predicción de Fidelización - Magda Monroy Jiménez
"""

import pandas as pd
import numpy as np

def get_customer_segment(recency, frequency, monetary, probability):
    """
    Segmentación RFM + Probabilidad para recomendaciones de negocio
    """
    
    # Segmentación RFM tradicional mejorada
    if recency <= 30 and frequency >= 8 and monetary >= 1000:
        if probability >= 0.8:
            return "Champions", "🏆", "#28a745"
        else:
            return "Loyal Customers", "💎", "#17a2b8"
    
    elif recency <= 60 and frequency >= 5 and monetary >= 500:
        if probability >= 0.7:
            return "Potential Loyalists", "⭐", "#ffc107"
        else:
            return "New Customers", "🌱", "#6f42c1"
    
    elif recency <= 90 and frequency >= 3:
        if probability >= 0.6:
            return "Promising", "📈", "#fd7e14"
        else:
            return "Need Attention", "⚠️", "#dc3545"
    
    elif recency > 90 and frequency >= 2:
        return "At Risk", "🚨", "#e83e8c"
    
    else:
        return "Lost", "💔", "#6c757d"

def get_business_recommendations(segment, recency, frequency, monetary, probability):
    """
    Recomendaciones específicas de negocio por segmento
    """
    
    recommendations = {
        "Champions": {
            "strategy": "Reward & Retain",
            "actions": [
                "🎁 Programa VIP exclusivo",
                "💰 Descuentos por volumen (15-20%)",
                "🚀 Early access a nuevos productos",
                "📞 Atención personalizada premium"
            ],
            "budget": "Alto",
            "priority": "Máxima",
            "roi_expected": "300-500%"
        },
        
        "Loyal Customers": {
            "strategy": "Nurture & Upsell",
            "actions": [
                "🛍️ Cross-selling personalizado",
                "💳 Programa de puntos premium",
                "📧 Newsletter exclusivo",
                "🎯 Ofertas en categorías favoritas"
            ],
            "budget": "Alto",
            "priority": "Alta",
            "roi_expected": "200-300%"
        },
        
        "Potential Loyalists": {
            "strategy": "Develop & Convert",
            "actions": [
                "📱 Onboarding personalizado",
                "🎁 Descuento en segunda compra (10%)",
                "📊 Recomendaciones basadas en historial",
                "⏰ Recordatorios de recompra"
            ],
            "budget": "Medio",
            "priority": "Alta",
            "roi_expected": "150-250%"
        },
        
        "New Customers": {
            "strategy": "Educate & Engage",
            "actions": [
                "👋 Welcome series (3 emails)",
                "🎁 Descuento de bienvenida (5-10%)",
                "📚 Guías de producto",
                "💬 Encuesta de satisfacción"
            ],
            "budget": "Medio",
            "priority": "Media",
            "roi_expected": "100-150%"
        },
        
        "Promising": {
            "strategy": "Activate & Motivate",
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
        
        "Need Attention": {
            "strategy": "Re-engage & Win Back",
            "actions": [
                "💌 Campaña de reactivación",
                "🎁 Oferta especial (15-25%)",
                "📋 Encuesta de feedback",
                "🆕 Mostrar nuevos productos"
            ],
            "budget": "Bajo-Medio",
            "priority": "Media",
            "roi_expected": "50-100%"
        },
        
        "At Risk": {
            "strategy": "Win Back Urgently",
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
        
        "Lost": {
            "strategy": "Last Chance Recovery",
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
    
    return recommendations.get(segment, recommendations["Lost"])

def calculate_customer_value_score(recency, frequency, monetary, probability):
    """
    Calcular score de valor del cliente (0-100)
    """
    # Normalizar métricas (0-1)
    recency_score = max(0, (365 - recency) / 365)  # Más reciente = mejor
    frequency_score = min(1, frequency / 20)  # Normalizar a máximo 20 compras
    monetary_score = min(1, monetary / 5000)  # Normalizar a máximo £5000
    
    # Pesos: Probabilidad 40%, Monetary 30%, Frequency 20%, Recency 10%
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
        "Champions": 50,
        "Loyal Customers": 35,
        "Potential Loyalists": 25,
        "New Customers": 15,
        "Promising": 20,
        "Need Attention": 12,
        "At Risk": 8,
        "Lost": 3
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
