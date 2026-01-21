import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

# Configuration
BROKER = "localhost"
PORT = 1883  # Fix: Utilisation du port 1883 car Mosquitto tourne sur ce port
INPUT_TOPIC = "wind/turbine/data/#"
OUTPUT_TOPIC = "wind/turbine/clean"

# Moyennes pour le nettoyage (remplacement des NaN/None)
MEANS = {
    "Wind speed (m/s)": 6.0,
    "Power (kW)": 500.0,
    "Energy Export (kWh)": 120.0
}

def clean_data(data):
    clean = {}
    for k, v in data.items():
        if (v is None or v == "") and k in MEANS:
            clean[k] = MEANS[k]
        else:
            clean[k] = v
    return clean

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✓ Connected to MQTT Broker on port {PORT}")
        client.subscribe(INPUT_TOPIC)
    else:
        print(f"✗ Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload["data"] = clean_data(payload["data"])
        payload["status"] = "cleaned"
        client.publish(OUTPUT_TOPIC, json.dumps(payload))
        print(f"✓ Nettoyé et re-publié: {payload.get('turbine_id')}")
    except Exception as e:
        print(f"Erreur: {e}")

# Initialisation avec la nouvelle API pour éviter les warnings
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print(f"Starting MQTT Cleaner (Port: {PORT})...")
try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"ERREUR CRITIQUE : Impossible de se connecter au broker sur le port {PORT}. Vérifiez que Mosquitto est bien lancé.")
    print(f"Détail : {e}")


