# MDS9_Palladium_TFM

Modelo de Predicción de Cancelaciones de Hotelles Palladium en América

Este repositorio contiene el Trabajo de Fin de Máster desarrollado para Palladium Hotel Group, centrado en la construcción de un modelo predictivo de cancelaciones de reservas.

Resumen del Proyecto:
A partir de un dataset inicial medianamente sucio de 1,4 millones de registros con más de 40 variables numéricas y categóricas (No incluido de acuerdo con la LOPD), se ha llevado a cabo un proceso completo de:
- Análisis exploratorio de datos (EDA)
- Limpieza y transformación de datos
- Feature engineering
- Desarrollo y validación de modelos

El modelo final se basa en LightGBM con validación cruzada, optimización de hiperparámetros y stacking segmentado en tres subgrupos, logrando una accuracy superior al 82% sobre un conjunto de test (20% del dataset, reservado exclusivamente para métricas. Data leakage cuidadosamente evitado).

Características:
- Código completamente anotado y autoexplicativo.
- Producto de datos desplegado en la nube y funcional.
- Estructura modular para facilitar su mantenimiento y escalabilidad.
