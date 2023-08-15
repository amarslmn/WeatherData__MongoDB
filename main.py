import pymongo
from pymongo import MongoClient
import json
from datetime import datetime
import requests
import logging
from dotenv import load_dotenv
import os



class GetDataWeather:

    """Classe pour récupérer les données météorologiques depuis l'API OpenWeatherMap."""
    def __init__(self, lon, lat, api_key):
        
        self.lat= lat
        self.lon = lon
        self.api_key = api_key
        self.url = f'https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}'


    def get_data_from_API(self):
    
        """
        Récupère les données météorologiques depuis l'API OpenWeatherMap.

        Returns:
            dict: Les données météorologiques sous forme de dictionnaire, ou None en cas d'erreur.
        """
        try:
            response = requests.get(self.url)
            

            if response.status_code == 200 or response.status_code == 201:
                logging.info("La requête a été traitée avec succès. Code de réponse : %s", response.status_code)
                return response.json()
            else:
                logging.warning("La requête a abouti, mais le code de réponse est %s.", response.status_code)
                return None

        except requests.exceptions.RequestException as e:
            logging.error("Une erreur s'est produite lors de la requète : : %s", e)
            return None

        except  Exception as ex:
            logging.error("Une erreur s'est produite lors de la récupération des données :%s", ex)
            return None


    def filter_data(self):
        """
        Filtre les données météorologiques récupérées.

        Returns:
            dict: Les données météorologiques filtrées sous forme de dictionnaire.
        """

        try:
            data = self.get_data_from_API()
            if data:
                logging.info("Récupération du dictionnaire de données météo pour les filtrer")
                data_filtred = {
                                    'Time': data['dt'],
                                    'Weather': data['weather'][0]['main'],
                                    'Rain Volume (mm)': data.get('rain', {}).get('1h', 0),
                                    'Temperature (Celsius)' : round(data['main']['temp'] - 273.15, 2),
                                    'Wind Speed (m/s)': data['wind']['speed'],
                                    'Humidity (%)': data['main']['humidity'],
                                    'Station Name' : data['name']
                                }
                logging.info("Renvoie du dictionnaire de données météo filtrées")
                return data_filtred
        
        except Exception as e:
            logging.error("Erreur lors de la filtration des données météto : %s", e)



class Insert_to_Database:
    """Classe pour insérer les données filtrées dans la base de données MongoDB."""

    def __init__(self,connection_string: str, name_database: str, name_collection: str, lon: str, lat: str, api_key: str):
        """
        Initialise une instance de Insert_to_Database.

        Args:
            connection_string (str): La chaîne de connexion à la base de données MongoDB.
            name_database (str): Le nom de la base de données.
            name_collection (str): Le nom de la collection.
            lon (str): La longitude géographique.
            lat (str): La latitude géographique.
            api_key (str): La clé API pour accéder à l'API OpenWeatherMap.
        """

        self.connection_string= connection_string
        self.name_database = name_database
        self.name_collection = name_collection
        try : 

            self.client = MongoClient(self.connection_string)
            self.database = self.client[self.name_database]
            self.collection = self.database[self.name_collection]
            
        
            logging.info("Connexion à MongoDB établie avec succès")

        except Exception as e:
            logging.error("Erreur lors de la connexion à MongoDB : %s", e)
        
        try:

            self.getdataweather= GetDataWeather(lat=lat, lon=lon, api_key=api_key)
            logging.info("Instance de la classe GetDataWeather créée")

        except Exception as e:
            logging.error("Erreur lors de la création de l'instanc de la classe GetDataWeather: %s", e)

    def insert_data(self):

        """
        Insère les données filtrées dans la base de données MongoDB.
        """
        try:
            data = self.getdataweather.filter_data()
            result = self.collection.insert_one(data)
            logging.info("Données insérées avec succès. ID du document : %s", result.inserted_id)

        except Exception as e:
            logging.error("Erreur lors de l'insertion des données : %s", e)




# Configuration de la journalisation
logging.basicConfig(level=logging.DEBUG,  #
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


# charger les variables d'environement
load_dotenv()
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
connection_string = os.getenv("CONNECTION_STRING")


with open("config.json", "r") as config_file:
    config = json.load(config_file)

weather_data = Insert_to_Database(
                                    connection_string=connection_string, 
                                    name_database=config["name_database"],
                                    name_collection=config["name_collection"],
                                    lat=config["lat"],
                                    lon=config["lon"],
                                    api_key=openweather_api_key)

weather_data.insert_data()