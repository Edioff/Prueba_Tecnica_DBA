import psycopg2
import random
import json  # <-- para convertir dict a JSON
from datetime import datetime, timedelta
import time

# Configuración de conexión a PostgreSQL
DB_CONFIG = {
    "dbname": "db",        
    "user": "postgres",
    "password": "jond887788",
    "host": "localhost",
    "port": "5432"
}

def insertar_usuarios(cursor, cantidad=100000):
    try:
        print(f"Insertando {cantidad} usuarios...")
        start_time = time.time()
        for i in range(1, cantidad + 1):
            cursor.execute("""
                INSERT INTO Usuarios (nombre, correo, saldo)
                VALUES (%s, %s, %s);
            """, (
                f"Usuario_{i}",
                f"usuario_{i}@example.com",
                random.uniform(10.0, 1000.0)
            ))
        end_time = time.time()
        print(f"Tiempo en insertar usuarios: {end_time - start_time:.2f} s")
    except psycopg2.Error as e:
        print(f"Error al insertar usuarios: {e}")
        cursor.connection.rollback()  # Deshacer cualquier cambio si ocurre un error
    except Exception as e:
        print(f"Error inesperado al insertar usuarios: {e}")
        cursor.connection.rollback()

def insertar_eventos(cursor, cantidad=10):
    try:
        print(f"Insertando {cantidad} eventos...")
        start_time = time.time()
        deportes = ["Fútbol", "Tenis", "Baloncesto", "Béisbol"]
        for i in range(1, cantidad + 1):
            tipo_deporte = random.choice(deportes)
            equipos = {
                "equipo1": f"Equipo_{2*i - 1}",
                "equipo2": f"Equipo_{2*i}"
            }
            # Convertir el dict a cadena JSON
            equipos_json = json.dumps(equipos)
            
            fecha_hora = datetime.now() + timedelta(days=random.randint(0, 30))
            cursor.execute("""
                INSERT INTO Eventos (tipo_deporte, equipos_participantes, fecha_hora)
                VALUES (%s, %s, %s);
            """, (tipo_deporte, equipos_json, fecha_hora))
        end_time = time.time()
        print(f"Tiempo en insertar eventos: {end_time - start_time:.2f} s")
    except psycopg2.Error as e:
        print(f"Error al insertar eventos: {e}")
        cursor.connection.rollback()
    except Exception as e:
        print(f"Error inesperado al insertar eventos: {e}")
        cursor.connection.rollback()

def insertar_apuestas(cursor, cantidad=500000, eventos=10, usuarios=100000):
    try:
        print(f"Insertando {cantidad} apuestas...")
        start_time = time.time()
        for _ in range(cantidad):
            cursor.execute("""
                INSERT INTO Apuestas (usuario_id, evento_id, monto_apostado, cuota, resultado, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                random.randint(1, usuarios),
                random.randint(1, eventos),
                random.uniform(5.0, 500.0),
                random.uniform(1.5, 5.0),
                random.choice(["ganada", "perdida"]),
                datetime.now() - timedelta(minutes=random.randint(0, 1440))
            ))
        end_time = time.time()
        print(f"Tiempo en insertar apuestas: {end_time - start_time:.2f} s")
    except psycopg2.Error as e:
        print(f"Error al insertar apuestas: {e}")
        cursor.connection.rollback()
    except Exception as e:
        print(f"Error inesperado al insertar apuestas: {e}")
        cursor.connection.rollback()

def main():
    conn = None
    cursor = None
    try:
        # Intentar conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos.")

        start_total = time.time()

        # 1. Insertar Usuarios
        insertar_usuarios(cursor)
        conn.commit()

        # 2. Insertar Eventos
        insertar_eventos(cursor)
        conn.commit()

        # 3. Insertar Apuestas
        insertar_apuestas(cursor)
        conn.commit()

        end_total = time.time()
        print(f"\nTiempo total de la simulación: {end_total - start_total:.2f} s")

    except psycopg2.OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado en el proceso principal: {e}")
    finally:
        if cursor:
            try:
                cursor.close()  # Intentar cerrar el cursor
                print("Cursor cerrado correctamente.")
            except Exception as e:
                print(f"Error al cerrar el cursor: {e}")
        
        if conn:
            try:
                conn.close()  # Intentar cerrar la conexión
                print("Conexión cerrada correctamente.")
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")

        print("\nDatos simulados insertados exitosamente.")

if __name__ == "__main__":
    main()
