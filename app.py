import sqlite3
import streamlit as st
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect("huellacarbono.db")

# Crear un cursor
cursor = conn.cursor()

# Consultar todas las tablas en la base de datos
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
cursor.execute(tables_query)
tables = cursor.fetchall()

# Inspeccionar la estructura de una tabla específica
tabla_seleccionada = st.selectbox("Selecciona una tabla para inspeccionar:", [table[0] for table in tables])

if tabla_seleccionada:
    st.write(f"Estructura de la tabla {tabla_seleccionada}:")
    estructura_query = f"PRAGMA table_info({tabla_seleccionada});"
    cursor.execute(estructura_query)
    estructura = cursor.fetchall()

    # Convertir los resultados en un DataFrame para mejor visualización
    df_estructura = pd.DataFrame(estructura, columns=["id", "Nombre", "Tipo", "NotNull", "Default", "PrimaryKey"])
    st.table(df_estructura[["Nombre", "Tipo"]])  # Mostrar solo columnas relevantes


# Barra de entrada para consultas personalizadas
st.write("### Realizar consultas personalizadas")
consulta = st.text_input("Escribe tu consulta SQL:", placeholder="Ejemplo: SELECT * FROM mi_tabla LIMIT 10")

if consulta:
    try:
        cursor.execute(consulta)
        resultados = cursor.fetchall()

        if resultados:
            # Obtener los nombres de las columnas
            columnas = [desc[0] for desc in cursor.description]
            # Convertir los resultados en un DataFrame
            df_resultados = pd.DataFrame(resultados, columns=columnas)
            st.table(df_resultados)  # Mostrar los resultados en una tabla
        else:
            st.write("La consulta no devolvió resultados.")
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")