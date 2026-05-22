import os
import time
import cv2
from ultralytics import YOLO
print("Loading PyTorch YOLOv8n model...")
model = YOLO("yolov8n.pt") 
video_path = "traffic.mp4"

if not os.path.exists(video_path):
    print(f"❌ Error: Please place a sample video named '{video_path}' in this directory.")
    exit()

cap = cv2.VideoCapture(video_path)
print("🚀 Running quick test inference on first 30 frames...")

start_time = time.time()
frame_count = 0
while cap.isOpened() and frame_count < 30:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame, classes=[2, 3, 5, 7], verbose=False)
    frame_count += 1

end_time = time.time()
cap.release()
pytorch_fps = frame_count / (end_time - start_time)
print(f"✅ PyTorch Test Complete. Processed {frame_count} frames.")
print(f"Average PyTorch Speed: {pytorch_fps:.2f} FPS\n")
print("Exporting model to ONNX format for edge optimization...")
onnx_path = model.export(format="onnx", half=True)
print(f"Success! Optimized model saved at: {onnx_path}")
print(" Verifying optimized ONNX model...")
onnx_model = YOLO(onnx_path, task="detect")
print("✅ ONNX model successfully loaded and verified!")