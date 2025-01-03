# 📌 Prueba Técnica de DBA

Este repositorio contiene la solución a la prueba técnica de DBA. Se han implementado consultas SQL, triggers en PostgreSQL y pipelines ETL en PySpark para la detección de patrones sospechosos en apuestas.

📄 **Documentación completa en Notion:** [🔗 Ver Documento](https://mangrove-red-378.notion.site/Prueba-T-cnica-16f48925011e80b0a626f8089a1454e3)

---

## 📁 Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas:

Prueba_tecnica_dba/ │── python/ # Scripts ETL en PySpark │ ├── pipeline_2_1.py # Detecta usuarios con más de 50 apuestas en 10 minutos │ ├── pipeline_2_2.py # Detecta más de 20 apuestas idénticas en 5 minutos │ ├── simulacion_datos.py # Generación de datos de prueba │ │── recursos/ # Dependencias necesarias │ ├── postgresql-42.7.4.jar # Driver JDBC para PostgreSQL │ │── sql/ # Scripts SQL organizados por categoría │ ├── esquema/ # Definición de tablas y relaciones │ ├── indices/ # Creación de índices optimizados │ ├── patrones/ # Consultas SQL para detección de patrones │ ├── triggers/ # Implementación de triggers en PostgreSQL

yaml
Copiar código

---

## 🚀 Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

- **PostgreSQL** (mínimo versión 12)
- **Python 3.8+**
- **Apache Spark** con PySpark
- **Conector JDBC para PostgreSQL** (`postgresql-42.7.4.jar`)

Para instalar dependencias en Python:

```sh
pip install pyspark psycopg2 pandas
🔧 Configuración
Antes de ejecutar los scripts, modifica las credenciales de conexión en los archivos Python para que coincidan con tu base de datos:

python
Copiar código
DB_CONFIG = {
    "dbname": "db",
    "user": "postgres",
    "password": "tu_contraseña",
    "host": "localhost",
    "port": "5432"
}
⚠️ IMPORTANTE:

Es necesario modificar el nombre de la base de datos, usuario, contraseña, host y puerto en la configuración de psycopg2 y JDBC en los archivos pipeline_2_1.py, pipeline_2_2.py y simulacion_datos.py.
También es posible que debas ajustar los directorios donde están almacenados los archivos de recursos (recursos/postgresql-42.7.4.jar).
🛠️ Instrucciones de Uso
1️⃣ Configurar PostgreSQL
Ejecutar los scripts en sql/esquema/ para crear las tablas.
2️⃣ Crear Índices
Ejecutar los scripts en sql/indices/ para optimizar el rendimiento.
3️⃣ Configurar los Triggers
Ejecutar los archivos en sql/triggers/ para activar la detección automática de patrones.
4️⃣ Ejecutar los Pipelines ETL en PySpark
Para analizar las apuestas y detectar patrones sospechosos:

sh
Copiar código
python python/pipeline_2_1.py  # Detecta usuarios con más de 50 apuestas en 10 minutos
python python/pipeline_2_2.py  # Detecta más de 20 apuestas idénticas en 5 minutos
5️⃣ Consultar Patrones Detectados
Se pueden visualizar los patrones sospechosos ejecutando las queries en sql/patrones/.
📊 Resultados y Optimización
Se utilizaron índices y EXPLAIN ANALYZE para optimizar las consultas. Se analizaron los triggers de PostgreSQL, evaluando su impacto en el rendimiento:

Tiempo de ejecución de los triggers en Apuestas:
Patrón 2.1 (Usuarios con +50 apuestas en 10 minutos) → ~1.985 ms
Patrón 2.2 (Más de 20 apuestas idénticas en 5 minutos) → ~0.090 ms
📊 Más detalles en el análisis de rendimiento: 🔗 Ver Documento en Notion

💡 Mejoras Futuras
🔹 Optimizar las consultas para manejar grandes volúmenes de datos.
🔹 Implementar particionamiento en la base de datos.
🔹 Evaluar una arquitectura basada en Apache Kafka + Spark Streaming para detección en tiempo real.
