import json
import psycopg2
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "edge/telemetry/traffic"

DB_HOST = "localhost"
DB_NAME = "traffic_metrics"
DB_USER = "postgres"
DB_PASSWORD = "password123"
print("🐘 Connecting to TimescaleDB...")
conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicle_telemetry (
    time TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(50) NOT NULL,
    vehicle_count INT NOT NULL,
    inference_time_ms REAL NOT NULL
);
""")
try:
    cursor.execute("SELECT create_hypertable('vehicle_telemetry', 'time', if_not_exists => TRUE);")
except Exception:
    pass
conn.commit()
print("✅ Database schema initialized.")
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"📡 Worker connected to MQTT. Subscribing to: {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        
        # Insert into time-series database
        insert_query = """
        INSERT INTO vehicle_telemetry (time, device_id, vehicle_count, inference_time_ms)
        VALUES (TO_TIMESTAMP(%s), %s, %s, %s);
        """
        cursor.execute(insert_query, (
            data["timestamp"], 
            data["device_id"], 
            data["vehicle_count"], 
            data["inference_time_ms"]
        ))
        conn.commit()
        print(f"💾 Persisted telemetry data row from {data['device_id']}")
        
    except Exception as e:
        print(f"❌ Error persisting data: {e}")
        conn.rollback()
# client = mqtt.Client(callback_api_version=mqtt.CallbackApiVersion.VERSION2)
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
print("🔄 Ingestion worker running. Awaiting messages...")
client.loop_forever()