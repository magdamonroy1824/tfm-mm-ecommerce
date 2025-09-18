# Notebooks del Proyecto de Fidelización

Este directorio contiene los notebooks de Jupyter que implementan el pipeline completo del proyecto de predicción de clientes fidelizables en e-commerce.

## Orden de Ejecución

Los notebooks deben ejecutarse en el siguiente orden:

### 1. `01_exploratory_data_analysis.ipynb`
**Análisis Exploratorio de Datos**
- Carga inicial del dataset Online Retail
- Análisis de calidad de datos y valores faltantes
- Exploración de patrones temporales y de clientes
- Estadísticas descriptivas básicas

**Salidas:**
- Visualizaciones exploratorias
- Resumen de la estructura de datos

### 2. `02_data_preprocessing.ipynb`
**Preprocesamiento de Datos**
- Limpieza de datos (valores faltantes, outliers)
- Eliminación de transacciones canceladas
- Creación de variables derivadas básicas
- Tratamiento de inconsistencias

**Salidas:**
- `data/processed/online_retail_clean.csv`

### 3. `03_feature_engineering.ipynb`
**Ingeniería de Características**
- Cálculo de métricas RFM (Recency, Frequency, Monetary)
- Creación de características de comportamiento de compra
- Definición de la variable objetivo (cliente fidelizable)
- Agregación de datos por cliente

**Salidas:**
- `data/processed/customer_features.csv`

### 4. `04_google_trends_integration.ipynb`
**Integración con Google Trends**
- Obtención de datos de tendencias de búsqueda
- Alineación temporal con transacciones
- Creación de características basadas en tendencias externas
- Análisis de correlación con fidelización

**Salidas:**
- `data/processed/customer_features_with_trends.csv`
- `data/external/google_trends_data.csv`

### 5. `05_model_development.ipynb`
**Desarrollo del Modelo**
- Preparación de datos para modelado
- Selección de características
- Entrenamiento de múltiples algoritmos
- Optimización de hiperparámetros
- Selección del mejor modelo

**Salidas:**
- `results/models/best_loyalty_model.pkl`
- `results/models/feature_scaler.pkl`
- `results/models/feature_selector.pkl`
- `results/models/model_info.json`

### 6. `06_model_evaluation.ipynb`
**Evaluación del Modelo**
- Métricas de clasificación completas
- Análisis ROC-AUC y curvas de rendimiento
- Matriz de confusión
- Importancia de características
- Análisis de errores

**Salidas:**
- `results/figures/confusion_matrix.png`
- `results/figures/roc_pr_curves.png`
- `results/figures/feature_importance.png`
- `results/reports/evaluation_summary.json`

### 7. `07_business_insights.ipynb`
**Insights de Negocio**
- Segmentación de clientes basada en probabilidades
- Identificación de patrones de fidelización
- Recomendaciones estratégicas
- Preparación de datos para dashboard

**Salidas:**
- `results/reports/business_insights.json`
- `data/processed/tableau_export.csv`

## Requisitos

Antes de ejecutar los notebooks, asegúrate de:

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Descargar el dataset:**
   - Descargar el dataset Online Retail desde: https://archive.ics.uci.edu/dataset/352/online+retail
   - Colocar el archivo `online_retail.xlsx` en `data/raw/`

3. **Configurar Google Trends (opcional):**
   - Los notebooks incluyen datos sintéticos como fallback
   - Para datos reales, verificar conectividad a Google Trends API

## Estructura de Datos

### Dataset Principal: Online Retail
- **InvoiceNo**: Número de factura
- **StockCode**: Código de producto
- **Description**: Descripción del producto
- **Quantity**: Cantidad comprada
- **InvoiceDate**: Fecha de la transacción
- **UnitPrice**: Precio unitario
- **CustomerID**: ID único del cliente
- **Country**: País del cliente

### Variables Objetivo
- **IsLoyal**: Variable binaria (1 = fidelizable, 0 = no fidelizable)
- **Loyalty_Probability**: Probabilidad de fidelización (0-1)
- **Loyalty_Segment**: Segmento de fidelización

## Notas Técnicas

- **Memoria**: Los notebooks están optimizados para datasets de tamaño medio
- **Tiempo de ejecución**: El pipeline completo toma aproximadamente 30-45 minutos
- **Reproducibilidad**: Se usa `random_state=42` en todos los procesos aleatorios
- **Visualizaciones**: Se guardan automáticamente en `results/figures/`

## Troubleshooting

### Problemas Comunes

1. **Error al cargar datos:**
   - Verificar que `online_retail.xlsx` esté en `data/raw/`
   - Comprobar permisos de lectura del archivo

2. **Error de Google Trends:**
   - Los notebooks funcionan con datos sintéticos si falla la API
   - Verificar conectividad a internet

3. **Memoria insuficiente:**
   - Reducir el tamaño del dataset en el notebook 01
   - Usar muestreo estratificado si es necesario

4. **Dependencias faltantes:**
   - Ejecutar `pip install -r requirements.txt`
   - Verificar versiones de Python (recomendado: 3.8+)

## Contacto

Para preguntas sobre la implementación, consultar la documentación del proyecto principal en el README.md de la raíz.
