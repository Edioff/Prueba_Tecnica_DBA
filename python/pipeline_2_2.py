from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, count
import psycopg2
import time

try:
    # 1. Configuración de Spark
    spark = SparkSession.builder \
        .appName("ETL - Detección de Apuestas Idénticas (Patrón 2.2) con Tabla Temporal") \
        .config("spark.sql.shuffle.partitions", 200) \
        .config("spark.jars", "file:///C:/Users/Pc2/Desktop/Prueba_tecnica_dba/recursos/postgresql-42.7.4.jar") \
        .getOrCreate()

    # Ajusta según tu DB real
    jdbc_url = "jdbc:postgresql://localhost:5432/db"  
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

        # Crear tabla temporal para almacenar patrones idénticos
        cursor.execute("""
        CREATE TEMP TABLE temp_patrones_identicas (
            usuario_id        BIGINT NOT NULL,
            evento_id         BIGINT NOT NULL,
            monto_apostado    NUMERIC(12, 2) NOT NULL,
            cuota            NUMERIC(5, 2) NOT NULL,
            inicio_intervalo  TIMESTAMP NOT NULL,
            fin_intervalo     TIMESTAMP NOT NULL,
            total_apuestas    INT NOT NULL
        );
        """)
        conn.commit()
        print("Tabla temporal 'temp_patrones_identicas' creada exitosamente.")

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

        # 4. Detectar apuestas idénticas en intervalos de 5 minutos
        inicio_procesamiento = time.time()
        df_patrones = df_apuestas \
            .groupBy(
                window(col("timestamp"), "5 minutes"),
                col("evento_id"),
                col("monto_apostado"),
                col("cuota"),
                col("usuario_id")  # Incluir usuario si quieres registrarlo
            ) \
            .agg(count("*").alias("total_apuestas")) \
            .filter(col("total_apuestas") > 20) \
            .select(
                col("usuario_id"),
                col("evento_id"),
                col("monto_apostado"),
                col("cuota"),
                col("window.start").alias("inicio_intervalo"),
                col("window.end").alias("fin_intervalo"),
                col("total_apuestas")
            )
        fin_procesamiento = time.time()
        print(f"Tiempo de procesamiento: {fin_procesamiento - inicio_procesamiento:.2f} segundos")

        # **Muestra los resultados** (df_patrones) en consola
        print("\nResultados (Más de 20 apuestas idénticas en 5 minutos):")
        df_patrones.show(50, truncate=False)

        # 5. Guardar los resultados en la tabla temporal
        inicio_escritura = time.time()
        df_patrones.write \
            .format("jdbc") \
            .option("url", jdbc_url) \
            .option("dbtable", "temp_patrones_identicas") \
            .options(**db_properties) \
            .mode("append") \
            .save()
        fin_escritura = time.time()
        print(f"Tiempo de escritura: {fin_escritura - inicio_escritura:.2f} segundos")

        # **Consulta la tabla temporal antes de cerrar la conexión**
        cursor.execute("SELECT * FROM temp_patrones_identicas;")
        rows = cursor.fetchall()
        print("\nRegistros en la tabla temporal (temp_patrones_identicas):")
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
