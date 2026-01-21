# wind_turbine_data_pipeline
A real-time IoT data pipeline for wind turbines using MQTT, Redis, and MongoDB.
# 🌬️ Pipeline de Données Éoliennes en Temps Réel

Ce projet implémente un pipeline de données IoT complet pour surveiller et analyser les performances des éoliennes en temps réel. Il simule la génération de données, assure le nettoyage, le transit via un bus de messages, et le stockage final dans une base de données NoSQL.

## 🏗️ Architecture du Système

Le pipeline suit le flux suivant :
1.  Génération : Simulations Python publiant des données de télémétrie (Vitesse du vent, Puissance, Énergie).
2.  Transport (MQTT) : Utilisation de Mosquitto pour le passage de messages.
3.  Nettoyage (Cleaning) : Filtre les valeurs aberrantes et remplace les données manquantes.
4.  Buffer (Redis) : Mise en cache intermédiaire et streaming des données propres.
5.  Stockage (MongoDB) : Persistance long-terme pour analyse ultérieure.



## 📂 Structure du Projet

*   `Turibne_101_Data_Generator.py` : Simule les capteurs de l'éolienne 101.
*   `mqtt_cleaner.py` : Nettoie les données brutes (remplacement des `null` par les moyennes).
*   `mqtt_to_redis.py` : Transfère les flux propres vers Redis.
*   `redis_to_mongo.py` : Consomme Redis pour enregistrer les documents dans MongoDB.

## 🚀 Installation et Démarrage

### 1. Prérequis
Assurez-vous d'avoir installé :
*   **Python 3.x**
*   **Mosquitto MQTT Broker**
*   **Redis**
*   **MongoDB**

### 2. Installation des dépendances
```bash
pip install paho-mqtt redis pymongo numpy
```

### 3. Exécution (Ordre recommandé)
Ouvrez plusieurs terminaux et lancez les scripts dans cet ordre :

1.  **Le Broker MQTT & Services DB** (Assurez-vous qu'ils tournent)
2.  **L'abonné final (Persistence)** :
    ```bash
    python scripts_wind_turbine/redis_to_mongo.py
    ```
3.  **Le pont Redis** :
    ```bash
    python scripts_wind_turbine/mqtt_to_redis.py
    ```
4.  **Le nettoyeur de données** :
    ```bash
    python scripts_wind_turbine/mqtt_cleaner.py
    ```
5.  **Les générateurs** :
    ```bash
    python scripts_wind_turbine/Turibne_101_Data_Generator.py
    # ... répéter pour 102 et 103
    ```

## 📊 Format des Données (JSON)
Les données traitées ressemblent à :
```json
{
    "turbine_id": "T101",
    "timestamp": "2026-01-17 21:30:00",
    "wind_speed": 6.5,
    "power": 520.1,
    "energy": 130.0,
    "status": "cleaned"
}
```

## 🛠️ Technologies Utilisées
*   **Langage** : Python (Numpy, Paho-MQTT)
*   **Messaging** : MQTT (Mosquitto)
*   **Cache/Stream** : Redis
*   **Base de données** : MongoDB
