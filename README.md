# Edge-to-Cloud ML Telemetry & Analytics Pipeline

An end-to-end MLOps and ML Systems project that simulates a high-throughput traffic tracking infrastructure. The system features model optimization for edge deployment, real-time message streaming, containerized storage architecture, and data observability.

## 🏗️ System Architecture
1. **Edge Optimization Layer**: Employs a quantized, compiled **YOLOv8** model exported to **ONNX format** to reduce memory footprints and inference latency on edge environments.
2. **Streaming Broker**: An edge python runner captures local frame metrics (vehicle counts, processing speeds) and broadcasts lightweight JSON payloads via an **MQTT Broker (Eclipse Mosquitto)**.
3. **Ingestion & Database Worker**: A containerized subscriber captures streams asynchronously and sinks records down to **TimescaleDB** (time-series optimized PostgreSQL).
4. **Observability Layer**: A real-time **Grafana** engine aggregates database transactions to monitor inference metrics alongside pipeline system throughput.

## 🛠️ Tech Stack
- **Languages/Frameworks**: Python, FastAPI/OpenCV, ONNX Runtime, SQL
- **Infrastructure**: Docker & Docker Compose, MQTT (Mosquitto)
- **Data & Metrics**: TimescaleDB, Grafana