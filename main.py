import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
import requests

# Load konfigurasi dari .env
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)

URL_API_GREENAPI = os.getenv("URL_API_GREENAPI", None)
WHATSAPP_CHAT_ID = os.getenv("WHATSAPP_CHAT_ID", None)
WHATSAPP_GROUP_ID = os.getenv("WHATSAPP_GROUP_ID", None)


def send_to_whatsapp(data):
    url = URL_API_GREENAPI

    payload = {
    "chatId": f"{WHATSAPP_GROUP_ID}", 
    "message": f"{data}"
    }
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)

    print(response.text.encode('utf8'))
# Callback ketika berhasil terhubung ke broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Terhubung ke broker MQTT")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Gagal terhubung, kode error: {reason_code}")

# Callback ketika menerima pesan
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())  # Parsing JSON
        print(f"Pesan diterima dari {msg.topic}:")

        DEVICE_ID = payload.get("device_id", "Unknown")
        DEVICE_TYPE = payload.get("device_type", "Unknown")
        LOCATION = payload.get("location", "Unknown")
        TIMESTAMP = payload.get("timestamp", "Unknown")
        TEMPERATURE = payload.get("data", {}).get("temperature", "N/A")
        HUMIDITY = payload.get("data", {}).get("humidity", "N/A")
        VOLTAGE = payload.get("power_consumption", {}).get("voltage", "N/A")
        CURRENT = payload.get("power_consumption", {}).get("current", "N/A")
        POWER = payload.get("power_consumption", {}).get("power", "N/A")
        BATTERY = payload.get("battery_level", "N/A")
        
        # Format pesan agar lebih rapi dalam bentuk kolom
        formatted_data = (
            f"📡 *Device Info* 📡\n"
            f"──────────────────────\n"
            f"📌 *Device ID*   : {DEVICE_ID}\n"
            f"🔎 *Device Type* : {DEVICE_TYPE}\n"
            f"📍 *Location*    : {LOCATION}\n"
            f"⏳ *Timestamp*   : {TIMESTAMP}\n"
            f"──────────────────────\n"
            f"🌡️ *Temperature* : {TEMPERATURE}°C\n"
            f"💦 *Humidity*    : {HUMIDITY}%\n"
            f"⚡ *Voltage*     : {VOLTAGE}V\n"
            f"⚡ *Current*     : {CURRENT}A\n"
            f"🔌 *Power*       : {POWER}W\n"
            f"🔋 *Battery*     : {BATTERY}%\n"
            f"──────────────────────"
        )

        send_to_whatsapp(formatted_data)
    except json.JSONDecodeError:
        print(f"Pesan tidak valid: {msg.payload.decode()}")


# Inisialisasi klien MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Jika broker memerlukan autentikasi
if MQTT_USERNAME and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

# Koneksi ke broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Looping agar tetap menerima pesan
client.loop_forever()
