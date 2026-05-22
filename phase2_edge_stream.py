import os
import time
import json
import cv2
from ultralytics import YOLO
import paho.mqtt.client as mqtt

# --- CONFIGURATION ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "edge/telemetry/traffic"
VIDEO_PATH = "traffic.mp4"
ONNX_MODEL_PATH = "yolov8n.onnx"  
print("🔌 Connecting to Mosquitto MQTT Broker...")
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
if not os.path.exists(ONNX_MODEL_PATH):
    print(f"❌ Optimized ONNX model not found! Running default fallback...")
    ONNX_MODEL_PATH = "yolov8n.pt"

print(f"🤖 Loading optimized Edge model: {ONNX_MODEL_PATH}")
model = YOLO(ONNX_MODEL_PATH, task="detect")
cap = cv2.VideoCapture(VIDEO_PATH)
print("🚗 Processing video stream and broadcasting telemetry...")

try:
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        
        if not ret:

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        results = model(frame, classes=[2, 3, 5, 7], verbose=False)
        inference_time_ms = (time.time() - start_time) * 1000
        detected_boxes = results[0].boxes
        vehicle_count = len(detected_boxes) if detected_boxes is not None else 0
        payload = {
            "timestamp": int(time.time()),
            "device_id": "edge_node_cam_01",
            "vehicle_count": vehicle_count,
            "inference_time_ms": round(inference_time_ms, 2)
        }
        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"📡 Broadcasted: {payload}")
        time.sleep(0.03)

except KeyboardInterrupt:
    print("\n🛑 Stopping Edge Stream...")

finally:
    cap.release()
    client.loop_stop()
    client.disconnect()
    print("👋 Disconnected safely.")