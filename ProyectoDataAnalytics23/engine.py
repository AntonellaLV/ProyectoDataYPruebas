from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import pandas as pd


# Cadena de conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/ProyectoData23"  # Reemplaza username, password, dbname con tus propias credenciales y nombre de la base de datos

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

"""Modelo: # Configuración de la conexión a la base de datos
DATABASE_URL = "postgresql://username:password@localhost:5432/database_name"""

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Ciudad(Base):
    __tablename__ = 'ciudades'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)
    datos_climaticos = relationship('DatoClimatico', back_populates='ciudad')

class DatoClimatico(Base):
    __tablename__ = 'datos_climaticos'
    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    temperatura = Column(Float)
    humedad = Column(Float)
    descripcion_clima = Column(String)
    ciudad_id = Column(Integer, ForeignKey('ciudades.id'))
    ciudad = relationship('Ciudad', back_populates='datos_climaticos')

# Crear la tabla en la base de datos
Base.metadata.create_all(engine)

def create_weather_table(conn):
    # Código para crear la tabla 'weather_data' en PostgreSQL
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            date TIMESTAMP NOT NULL,
            temperature FLOAT NOT NULL,
            humidity INTEGER NOT NULL,
            weather_description VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    cursor.close()

def insert_weather_data(conn, data):
    # Código para insertar los datos en la tabla 'weather_data'
    cursor = conn.cursor()
    for item in data:
        cursor.execute("""
            INSERT INTO weather_data (city, date, temperature, humidity, weather_description)
            VALUES (%s, %s, %s, %s, %s)
        """, (item['city'], item['date'], item['temperature'], item['humidity'], item['weather_description']))
    conn.commit()
    cursor.close()

# Leer los datos de la tabla 'DatoClimatico' en un DataFrame
df_climatico = pd.read_sql_table('datos_climaticos', engine)

# Leer los datos de la tabla 'Ciudad' en un DataFrame
df_ciudades = pd.read_sql_table('ciudades', engine)

# Ver las primeras filas de los DataFrames:
print(df_climatico.head())
print(df_ciudades.head())

'''# Realizar estadísticas descriptivas:
print(df.describe())

# Ver las primeras filas del DataFrame:
print(df.head())

# Filtrar los datos por ciudad
city_name = "Nombre de la ciudad"
df_city = df[df['city'] == city_name]

# Filtrar los datos por rango de fechas:
start_date = "2023-01-01"
end_date = "2023-01-31"
df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

#Obtener el promedio de temperatura por ciudad:
df_avg_temperature = df.groupby('city')['temperature'].mean().reset_index()

# Visualizar los datos mediante gráficos:
# Gráfico de línea de la temperatura para una ciudad específica
city_name = "Nombre de la ciudad"
df_city = df[df['city'] == city_name]
plt.plot(df_city['date'], df_city['temperature'])
plt.xlabel('Fecha')
plt.ylabel('Temperatura (°C)')
plt.title(f'Temperatura en {city_name}')
plt.xticks(rotation=45)
plt.show()'''

