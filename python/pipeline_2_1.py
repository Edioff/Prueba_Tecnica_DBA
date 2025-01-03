from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, count
import psycopg2
import time

try:
    # 1. Configuración de Spark y PostgreSQL
    spark = SparkSession.builder \
        .appName("ETL - Detección de Patrones Sospechosos con Tabla Temporal") \
        .config("spark.sql.shuffle.partitions", 200) \
        .config("spark.jars", "file:///C:/Users/Pc2/Desktop/Prueba_tecnica_dba/recursos/postgresql-42.7.4.jar") \
        .getOrCreate()

    jdbc_url = "jdbc:postgresql://localhost:5432/db"  # Ajusta si tu DB se llama distinto
    db_properties = {
        "user": "postgres",
        "password": "jond887788",
        "driver": "org.postgresql.Driver"
    }

    inicio_etl = time.time()

    try:
        # 2. Conexión inicial a PostgreSQL para crear la tabla temporal
        conn = psycopg2.connect(
            dbname="db",
            user="postgres",
            password="jond887788",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Crear tabla temporal
        cursor.execute("""
        CREATE TEMP TABLE temp_patrones_sospechosos (
            usuario_id BIGINT NOT NULL,
            inicio_intervalo TIMESTAMP NOT NULL,
            fin_intervalo TIMESTAMP NOT NULL,
            apuestas_en_1_min INT NOT NULL
        );
        """)
        conn.commit()
        print("Tabla temporal creada exitosamente.")

        # 3. Leer datos desde PostgreSQL con Spark
        inicio_lectura = time.time()
        df_apuestas = spark.read \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "Apuestas") \
            .options(**db_properties) \
            .load()
        fin_lectura = time.time()
        print(f"Tiempo de lectura: {fin_lectura - inicio_lectura:.2f} segundos")

        # 4. Procesar apuestas en ventanas de 1 minuto
        inicio_procesamiento = time.time()
        df_patrones = df_apuestas \
            .groupBy(window(col("timestamp"), "1 minute"), col("usuario_id")) \
            .agg(count("*").alias("apuestas_en_1_min")) \
            .filter(col("apuestas_en_1_min") > 50) \
            .select(
                col("usuario_id"),
                col("window.start").alias("inicio_intervalo"),
                col("window.end").alias("fin_intervalo"),
                col("apuestas_en_1_min")
            )
        fin_procesamiento = time.time()
        print(f"Tiempo de procesamiento: {fin_procesamiento - inicio_procesamiento:.2f} segundos")

        # Muestra en consola los resultados detectados por Spark
        print("Resultados (más de 50 apuestas en 1 minuto) - df_patrones.show():")
        df_patrones.show(50, truncate=False)

        # 5. Guardar los resultados en la tabla temporal
        inicio_escritura = time.time()
        df_patrones.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "temp_patrones_sospechosos") \
            .options(**db_properties) \
            .mode("append") \
            .save()
        fin_escritura = time.time()
        print(f"Tiempo de escritura: {fin_escritura - inicio_escritura:.2f} segundos")

        # **Consulta la tabla temporal antes de cerrar la conexión**
        cursor.execute("SELECT * FROM temp_patrones_sospechosos;")
        rows = cursor.fetchall()
        print("\nRegistros en la tabla temporal (temp_patrones_sospechosos):")
        for row in rows:
            print(row)

    except Exception as e:
        print(f"Error durante el procesamiento del pipeline ETL: {e}")

    finally:
        # Cierra la conexión a PostgreSQL
        if conn:
            cursor.close()
            conn.close()

        fin_etl = time.time()
        print(f"Tiempo total del ETL: {fin_etl - inicio_etl:.2f} segundos")

except Exception as e:
    print(f"Error al inicializar Spark o la conexión a la base de datos: {e}")

finally:
    # Detener la sesión de Spark
    if 'spark' in locals():
        spark.stop()
        print("Sesión de Spark detenida.")
