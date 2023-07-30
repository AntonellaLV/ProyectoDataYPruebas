# API key de OpenWeatherMap
API_KEY = "0826c4779496abe5470b904311fa3097" #"cc3d07bf7909e147cd7443c0415b0f76" = API Demo
# URL base de la API de OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?" # "https://api.openweathermap.org/data/2.5/onecall/timemachine?" NO FUNCIONA # nivel medio Base de Datos.
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather" nivel inicial Base de Datos.
# Unidades para obtener los datos meteorológicos (por ejemplo, "metric" para Celsius)
UNITS = "metric"
FOLDER = 'data_analytics/openweather'
FILENAME = FOLDER + '/tiempodiario'

cityList = [
    "London",
    "New York",
    "Cordoba",
    "Taipei",
    "Buenos Aires",
    "Mexico City",
    "Dublin",
    "Tbilisi",
    "Bogota",
    "Tokio",
]

coordList = [
    "lat=31&lon=64",
    "lat=40&lon=-73",
    "lat=-31&lon=-64",
    "lat=25&lon=64",
    "lat=-34&lon=-58",
    "lat=19&lon=-99",
    "lat=53&lon=6",
    "lat=41&lon=44",
    "lat=4&lon=74",
    "lat=35&lon=139",
]
