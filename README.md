# Predicción de Clientes Fidelizables en E-commerce
## Trabajo Final de Máster - Data Science | Universidad Complutense de Madrid

### Descripción del Proyecto

Este proyecto desarrolla un modelo de clasificación binaria para predecir la probabilidad de fidelización de clientes en e-commerce, integrando variables internas del negocio con datos externos de Google Trends.

### Estructura del Proyecto

```
tfm-loyalty-prediction/
├── notebooks/                    # Notebooks de análisis secuencial (01-08)
├── data/                         # Datos organizados por etapa
│   ├── raw/                         # Datos originales (online_retail.xlsx)
│   ├── processed/                   # Datos procesados
│   └── external/                    # Datos de Google Trends
├── src/utils/                    # Utilidades reutilizables
├── results/                      # Resultados y artefactos
│   ├── models/                     # Modelos entrenados
│   ├── figures/                    # Visualizaciones generadas
│   └── reports/                    # Reportes de evaluación
├── demo_app.py                   # Aplicación web Streamlit
├── config.py                     # Configuración centralizada
├── requirements.txt              # Dependencias del proyecto
├── TFM_Moderado_20_Paginas.md    # Documento principal del TFM
└── README.md                     # Esta documentación
```

### Guía de Ejecución

#### 1. Configuración del Entorno
```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. Obtención de Datos
```bash
# Descargar Online Retail Dataset desde:
# https://archive.ics.uci.edu/dataset/352/online+retail
# Colocar 'online_retail.xlsx' en data/raw/
```

#### 3. Ejecución Secuencial de Notebooks
Los notebooks deben ejecutarse en orden:
1. **01_exploratory_data_analysis.ipynb** - Análisis exploratorio
2. **02_data_preprocessing.ipynb** - Limpieza y preprocesamiento
3. **03_feature_engineering.ipynb** - Creación de características RFM
4. **04_google_trends_integration.ipynb** - Integración de datos externos
5. **05_model_development.ipynb** - Desarrollo de modelos ML
6. **06_model_evaluation.ipynb** - Evaluación y métricas
7. **07_business_insights.ipynb** - Insights y recomendaciones
8. **08_customer_segmentation_business.ipynb** - Segmentación de clientes

#### 4. Aplicación Web Interactiva
```bash
# Ejecutar aplicación Streamlit
streamlit run demo_app.py
```

### Resultados Obtenidos

#### Rendimiento del Modelo
- **Modelo Final**: Random Forest con ROC-AUC de 0.847
- **Accuracy**: 84% en conjunto de prueba
- **F1-Score**: 0.82 (excelente balance)
- **Algoritmos Evaluados**: 6 modelos incluyendo Deep Learning

#### Aplicación Práctica
- **Dashboard Interactivo**: Streamlit con visualizaciones en tiempo real
- **Pipeline Productivo**: Código listo para implementación
- **Predicciones Integradas**: Visualizaciones que incorporan ML
- **Interfaz Intuitiva**: Fácil uso para stakeholders no técnicos

### Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Pandas & NumPy**: Manipulación de datos
- **Scikit-learn**: Algoritmos de Machine Learning
- **TensorFlow**: Redes neuronales profundas
- **Plotly**: Visualizaciones interactivas
- **Streamlit**: Aplicación web
- **PyTrends**: Integración con Google Trends

### Archivos Principales

- **TFM_Moderado_20_Paginas.md**: Documento completo del TFM
- **demo_app.py**: Aplicación web con predicciones en tiempo real
- **config.py**: Configuración centralizada del proyecto
- **notebooks/**: Pipeline completo de análisis y modelado
- **results/models/**: Modelos entrenados listos para uso

### Contacto

Trabajo Final de Máster  
Universidad Complutense de Madrid  
Máster en Big Data, Data Science e Inteligencia Artificial
