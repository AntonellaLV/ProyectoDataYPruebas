from weather_api import get_cities_weather_data
from engine import engine, create_weather_table
import pandas as pd

def main():
    cities_data = get_cities_weather_data()

    if cities_data:
        # Convertir la lista de datos climáticos en un DataFrame de Pandas
        df = pd.DataFrame(cities_data, columns=['city', 'date', 'temperature', 'humidity', 'weather_description'])
        # Establecer la conexión a la base de datos
        with engine.connect() as conn:
            # Crear la tabla si no existe
            create_weather_table(conn)
            # Insertar los datos climáticos en la tabla
            df.to_sql('weather_data', conn, if_exists='append', index=False)

        print("Datos climáticos almacenados en la base de datos.")
    else:
        print("No se encontraron datos climáticos para las ciudades y coordenadas predefinidas.")

if __name__ == "__main__":
    main()

'''def main():
    cities_data = get_cities_weather_data()

    # Aquí puedes realizar cualquier operación que desees con los datos climáticos obtenidos,
    # por ejemplo, imprimirlos en pantalla o realizar algún análisis.

    if cities_data:
        print("Datos climáticos obtenidos:")
        for data in cities_data:
            print(f"Ciudad: {data['city']}")
            print(f"Fecha y hora: {data['date']}")
            print(f"Temperatura: {data['temperature']}°C")
            print(f"Humedad: {data['humidity']}%")
            print(f"Descripción del clima: {data['weather_description']}")
            print("-" * 50)
    else:
        print("No se encontraron datos climáticos para las ciudades y coordenadas predefinidas.")

if __name__ == "__main__":
    main()'''
