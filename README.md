# Projet de Récupération et Stockage de Données Météo

Ce projet consiste à récupérer des données météorologiques en utilisant l'API OpenWeatherMap et à les stocker dans une base de données MongoDB. Le script Python utilise des classes pour encapsuler les fonctionnalités de récupération de données, de filtrage et d'insertion dans la base de données.

## Étapes pour exécuter le projet

1. Clonez ce dépôt sur votre machine locale.
2. Installez les dépendances en exécutant `pip install -r requirements.txt`.
3. Configurez les variables d'environnement en créant un fichier `.env` avec les informations suivantes :
   ```plaintext
   OPENWEATHER_API_KEY=xxxxxxxxxxxxxxx
   PSWD_DATABASE=xxxxxxxxxxxxxxxxxxxx
   CONNECTION_STRING=mongodb+srv://mongo:${PSWD_DATABASE}@clustertest.xxxxxxxx.mongodb.net/
4. Modifier le fichier config.json avec les informations de configuration, exemple : 
   ```plaintext
        {
            "name_database": "WeatherData",
            "name_collection": "London",
            "lat": "51.5074",
            "lon": "-0.1278"
        }
5. Exécutez le script principal en exécutant
  ```bash
     python main.py