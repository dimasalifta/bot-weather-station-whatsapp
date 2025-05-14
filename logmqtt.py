import paho.mqtt.client as mqtt
import csv
from datetime import datetime

# Konfigurasi broker dan topik
BROKER = "localhost"
PORT = 1883
TOPIC = "#"
CSV_FILE = "mqtt_log.csv"

# Buat file CSV dan tulis header jika belum ada
try:
    with open(CSV_FILE, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "topic", "payload"])
except FileExistsError:
    pass  # File sudah ada

# Callback saat terkoneksi ke broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

# Callback saat menerima pesan
def on_message(client, userdata, msg):
    timestamp = datetime.now().isoformat()
    topic = msg.topic
    payload = msg.payload.decode('utf-8', errors='replace')

    print(f"[{timestamp}] {topic} => {payload}")

    # Simpan ke CSV
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, topic, payload])

# Inisialisasi client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Koneksi ke broker
client.connect(BROKER, PORT, 60)

# Looping terus untuk menerima pesan
client.loop_forever()
