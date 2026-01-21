import json
import redis
import paho.mqtt.client as mqtt

# Configuration
BROKER = "localhost"
PORT = 1883
INPUT_TOPIC = "wind/turbine/clean"  # Écoute le flux NETTOYÉ
REDIS_CHANNEL = "wind_clean_stream"

# Connexion Redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT (Port {PORT}) - Waiting for clean data...")
        client.subscribe(INPUT_TOPIC)
    else:
        print(f"Connection failed: {rc}")

def on_message(client, userdata, msg):
    try:
        # On reçoit les données déjà nettoyées par mqtt_cleaner.py
        payload = json.loads(msg.payload.decode())
        
        # Publication vers Redis
        r.publish(REDIS_CHANNEL, json.dumps(payload))
        print(f"→ Redis: {payload['turbine_id']} acheminé")
        
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()

