import json
import redis
from pymongo import MongoClient
from datetime import datetime

# Connexion Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe("wind_clean_stream")

# Connexion MongoDB
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo.wind_farm
collection = db.turbine_data

print("Listening Redis and saving to MongoDB...")

for message in pubsub.listen():
    if message["type"] == "message":
        payload = json.loads(message["data"])

        doc = {
            "turbine_id": payload["turbine_id"],
            "timestamp": datetime.now(),
            "wind_speed": payload["data"].get("Wind speed (m/s)"),
            "power": payload["data"].get("Power (kW)"),
            "energy": payload["data"].get("Energy Export (kWh)")
        }

        collection.insert_one(doc)
        print("Saved to MongoDB:", doc["turbine_id"])
