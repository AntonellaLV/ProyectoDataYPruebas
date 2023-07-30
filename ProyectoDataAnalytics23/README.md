# Challenge Data Analytics - Nivel Inicial

## Nivel inicial, Nivel Medio Y Nivel Dificil:

1. Obtener el archivo de la fuente que escojamos archivos de fuente utilizando Google Colab y la librería requests, por último debe almacenarse en forma local en formato CSV:

Librerias necesarias:

```python
from datetime import datetime
import requests
import pandas as pd
from pandas import json_normalize
import json
```

### API de datos abiertos del clima:

Descripción: Algunas APIs públicas proporcionan datos históricos o en tiempo real sobre el clima, incluidas temperaturas, precipitaciones, vientos, etc.
API: https://openweathermap.org/api

1. Solicitud: Debes hacer una solicitud HTTP a la API para obtener los datos en formato JSON y luego convertirlos a CSV utilizando Python.

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

1. Organizar los archivos en rutas siguiendo la siguiente estructura:
“data_analytics\openweather\tiempodiario_yyyymmdd.csv”
La fecha de la nomenclatura es la fecha del tiempo tomado.
2. buscar estas ciudades:

```python
cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico City", "Dublin", "Tbilifis", "Bogota", "Tokio"]
coordList = ["lat=31&lon=64", "lat=40&lon=-73", "lat=-31&lon=-64", "lat=25&lon=64", "lat=-34&lon=-58", "lat=19&lon=-99", "lat=53&lon=6", "lat=41&lon=44", "lat=4&lon=74", "lat=35&lon=139"]
```

1. Realizar los comentarios correspondientes para una correcta comprensión del código. (#)

## Getting started
1. Es recomendable crear un entorno virtual e instalar las dependencias:

    Bash:
    ```bash
    python -m venv env
    source env/Scripts/activate
    pip install -r requirements.txt
    ```
    Windows cmd:
    ```cmd
    python -m venv env
    env/Scripts/activate
    pip install -r requirements.txt
    ```
## Nivel Medio:

2. Crear el archivo .env:
    
    ```ini
    api_key = Tu api key va aquí
    ```

3. Lanzar la app:
    ```bash
    python main.py
    ```
4. Para obtener los datos históricos del clima de 5 días para cada ciudad a través del endpoint onecall/timemachine, primero necesitas          
    '''modificar el BASE_URL en tu archivo config.py para que sea correcto. Debe incluir la API_KEY y el parámetro para obtener el histórico del clima. El BASE_URL debe quedar así:

    # config.py 
    Enpoint

    BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

el archivo weather_api.py, ajustar la función get_cities_weather_data() para hacer la solicitud a la API usando el nuevo endpoint y el rango de 5 días para cada ciudad.

Para normalizar la tabla, utilizar la función pd.json_normalize() de Pandas. Modificar la función get_cities_weather_data():

Agregar la configuración al archivo config.py y documentar el código con docstrings.

"""
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
        Exception: Si ocurre un error desconocido.
    """