import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from config import BASE_URL, API_KEY, UNITS, FOLDER, FILENAME, cityList, coordList
from alive_progress import alive_bar


# Obtener el tiempo actual en formato Unix
ts = int(datetime.now().timestamp())

def request_data(city: str = None, coord: dict = None):
    """
    Recibe "city" que es el nombre de la ciudad, en formato string
    o "coord" que es un diccionario con las coordenadas de la ciudad.
    Hace una solicitud a la API y si el código de respuesta es 200,
    devuelve los datos en formato JSON. De lo contrario, intentará manejar las excepciones.
    """

    try:
        if city:
            params = {"q": city, "units": UNITS, "appid": API_KEY}
            response = requests.get(BASE_URL, params)
        elif coord:
            lat, lon = coord['lat'], coord['lon']
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&dt={int(ts)}&appid={API_KEY}&units={UNITS}"
            response = requests.get(url)
        else:
            raise ValueError("Debe proporcionar 'city' o 'coord' como argumento.")

        response.raise_for_status()

        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    except KeyError as e:
        print(f"Error en el formato de respuesta de la API: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")
    return None

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
 
""" Nivel Inicial:
    Recibe "city" que es el nombre de la ciudad, en formato string
    Hace una solicitud a la api y si el código de respuesta
    Es 200, devuelve la data en formato json
    De lo contrario, intentará manejar las excepciones
    """
""" Nivel Medio:
    Realiza una solicitud a la API de OpenWeatherMap para obtener los datos climáticos de una ciudad o coordenadas.

    Args:
        city (str, opcional): Nombre de la ciudad para obtener los datos climáticos. 
                              Si no se proporciona, se utilizarán las coordenadas. Por defecto: None.
        coord (str, opcional): Coordenadas (latitud y longitud) para obtener los datos climáticos. 
                               Debe tener el formato "lat={lat}&lon={lon}". Por defecto: None.

    Returns:
        dict or None: Un diccionario con los datos climáticos si la solicitud fue exitosa,
                      None si ocurrió un error en la solicitud.

    Raises:
        requests.exceptions.RequestException: Si ocurre un error durante la solicitud a la API.
        KeyError: Si hay un error en el formato de respuesta de la API.
        Exception: Si ocurre un error desconocido.""" 
"""try:
        if city:
            params = {"q": city, "units": UNITS, "appid": API_KEY}

            response = requests.get(BASE_URL, params)
        else:
            response = requests.get(
                f"{BASE_URL}?{coord}&appid={API_KEY}&units={UNITS}"
            )

        response.raise_for_status()

        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    except KeyError as e:
        print(f"Error en el formato de respuesta de la API: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")"""

def export_to_json(data: list, filename: str):
    """Exportar datos a un archivo JSON."""
    with open(filename, "w") as file:
        json.dump(data, file)

def export_to_csv(data_list, filename):
    dfs = []
    for data in data_list:
        wdf = pd.json_normalize(data["weather"][0]).add_prefix("weather_")

        keys_to_remove = ["weather", "base", "timezone", "cod"]

        for key in keys_to_remove:
            del data[key]

        dfc = pd.json_normalize(data)

        dfc = pd.concat([dfc, wdf], axis=1)

        dfs.append(dfc)

    if len(dfs) > 0:
        df = pd.concat(dfs, axis=0)
        df.to_csv(filename, index=False)
    else:
        print("No hay datos válidos para exportar a CSV.")

def formatted_date_time():
    return datetime.now().strftime("%Y%m%d")

def format_datetime(unix_timestamp):

    # Convertir el tiempo Unix a una fecha y hora en UTC
    utc_datetime = datetime.utcfromtimestamp(unix_timestamp)

    gmt3_offset = timedelta(hours=-3)
    argentina_datetime = utc_datetime + gmt3_offset
    
    return argentina_datetime

'''def save_to_file(data, filename):
    with open(filename, "w") as file:
        file.write(data)
        file.close()'''

'''def get_cities_weather_data():
    """
    Obtener los datos del clima
    A partir de la lista de ciudades
    Devuelve un conjunto de respuestas
    """

    cities_data = []
    unreached_cities = []

    with alive_bar(len(cityList) + len(coordList), title='Processing', length=20, bar='bubbles') as bar:
        for city in cityList:
            bar()
            city_data = request_data(city=city)
            if city_data:
                # Obtener la fecha actual en formato Unix para el día actual
                ts = int(datetime.now().timestamp())

                # Solicitar datos históricos del clima de 5 días para cada ciudad
                for day in range(5):
                    # Calcular el timestamp para el día actual menos el número de días (day) en segundos
                    ts_day = ts - (day * 86400)
                    url = f"{BASE_URL}?lat={city_data['coord']['lat']}&lon={city_data['coord']['lon']}&dt={ts_day}&appid={API_KEY}&units={UNITS}"
                    response = requests.get(url).json()
                    if 'hourly' in response:
                        for hourly_data in response['hourly']:
                            data = {
                                'city': city_data['name'],
                                'date': datetime.utcfromtimestamp(hourly_data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                                'temperature': hourly_data['temp'],
                                'humidity': hourly_data['humidity'],
                                'weather_description': hourly_data['weather'][0]['description']
                            }
                            cities_data.append(data)
                    else:
                        unreached_cities.append(city)

    print("_" * 50)

    unreached_cities_filename = f"{FOLDER}/no_alcanzadas_{formatted_date_time()}.lst"
    weather_data_filename = f"{FILENAME}_{formatted_date_time()}.csv"

    export_to_json(unreached_cities, unreached_cities_filename)
    print(f"Se guardó la lista de ciudades no alcanzadas en {unreached_cities_filename}")

    export_to_csv(cities_data, weather_data_filename)
    print(f"Los datos del tiempo se guardaron en {weather_data_filename}")
    return cities_data'''


def get_cities_weather_data():

    """
    Obtener los datos del clima para todas las ciudades en cityList y coordList.
    Devuelve una lista con los datos climáticos de todas las ciudades.
    """

    cities_data = []
    unreached_cities = []

    with alive_bar(len(cityList) + len(coordList), title='Processing', length=20, bar='bubbles') as bar:
        for city in cityList:
            bar()
            city_data = request_data(city=city)
            if city_data:
                # Obtener la fecha actual en formato Unix para el día actual
                ts = int(datetime.now().timestamp())

                # Solicitar datos históricos del clima de 5 días para cada ciudad
                for day in range(5):
                    # Calcular el timestamp para el día actual menos el número de días (day) en segundos
                    ts_day = ts - (day * 86400)
                    url = f"{BASE_URL}?lat={city_data['coord']['lat']}&lon={city_data['coord']['lon']}&dt={ts_day}&appid={API_KEY}&units={UNITS}"
                    response = requests.get(url).json()
                    if 'hourly' in response:
                        for hourly_data in response['hourly']:
                            data = {
                                'city': city_data['name'],
                                'date': datetime.utcfromtimestamp(hourly_data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                                'temperature': hourly_data['temp'],
                                'humidity': hourly_data['humidity'],
                                'weather_description': hourly_data['weather'][0]['description']
                            }
                            cities_data.append(data)
                    else:
                        unreached_cities.append(city)

    print("_" * 50)

    unreached_cities_filename = f"{FOLDER}/no_alcanzadas_{formatted_date_time()}.lst"
    weather_data_filename = f"{FILENAME}_{formatted_date_time()}.csv"

    export_to_json(unreached_cities, unreached_cities_filename)
    print(f"Se guardó la lista de ciudades no alcanzadas en {unreached_cities_filename}")

    export_to_csv(cities_data, weather_data_filename)
    print(f"Los datos del tiempo se guardaron en {weather_data_filename}")
    return cities_data

'''def get_cities_weather_data():
    """
    Obtener los datos del clima
    A partir de la lista de ciudades
    Devuelve un conjunto de respuestas
    """

    cities_data = []

    with alive_bar(len(cityList) + len(coordList), title='Processing', length=20, bar='bubbles') as bar:
        for city in cityList:
            bar()
            city_data = request_data(city=city)
            if city_data:
                # Obtener la fecha actual en formato Unix
                ts = int(datetime.now().timestamp())

                # Solicitar datos históricos del clima de 5 días para cada ciudad
                for day in range(5):
                    url = f"{BASE_URL}?lat={city_data['coord']['lat']}&lon={city_data['coord']['lon']}&dt={ts}&appid={API_KEY}&units={UNITS}"
                    response = requests.get(url).json()
                    if 'hourly' in response:
                        for hourly_data in response['hourly']:
                            data = {
                                'city': city_data['name'],
                                'date': datetime.utcfromtimestamp(hourly_data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                                'temperature': hourly_data['temp'],
                                'humidity': hourly_data['humidity'],
                                'weather_description': hourly_data['weather'][0]['description']
                            }
                            cities_data.append(data)

    return cities_data

print("_" * 50)

unreached_cities_filename = (
        f"{FOLDER}/no_alcanzadas_{formatted_date_time()}.lst"
    )
weather_data_filename = f"{FILENAME}_{formatted_date_time()}.csv"

export_to_json(unreached_cities, unreached_cities_filename)
print(
        f"Se guardó la lista de ciudades no alcanzadas en {unreached_cities_filename}"
    )

export_to_csv(cities_data, weather_data_filename)
print(f"Los datos del tiempo se guardaron en {weather_data_filename}")

 return cities_data'''


    # Acá almacenamos los datos de todas las ciudades
    # Para luego ser exportadas

    
    # Código Nivel Inicial:
#'''cities_data = []
# unreached_cities = []
#with alive_bar(len(cityList)+len(coordList), title='Processing', length=20, bar='bubbles') as bar:
#for city in cityList:
 #           bar()
  #          city_data = request_data(city=city)
   #         if city_data:
    #            city_data["dt"] = format_datetime(city_data["dt"])
     #           cities_data.append(city_data)
      #      else:
       #         unreached_cities.append(city)
    #
    #
     #   for coord in coordList:
      #      bar()
       #     coord_data = request_data(coord=coord)
        #    if coord_data:
         #       coord_data["dt"] = format_datetime(coord_data["dt"])
          #      cities_data.append(coord_data)
           # else:
            #    unreached_cities.append(coord)'''