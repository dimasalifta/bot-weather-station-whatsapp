import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
# Load konfigurasi dari .env
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)

URL_API_GREENAPI = os.getenv("URL_API_GREENAPI", 'https://api.greenapi.com/waInstance7105242912/sendMessage/7ab1c9ec3fc448b280300ab4eab6d12e149762adb6ec43949c')
WHATSAPP_CHAT_ID = os.getenv("WHATSAPP_CHAT_ID", None)
WHATSAPP_GROUP_ID = os.getenv("WHATSAPP_GROUP_ID", '120363416927198799@g.us')

def estimate_battery_capacity(voltage, current, initial_capacity=12.0):
    soc_voltage = round(max(0, min(100, ((voltage - 11.0) / 3.4) * 100)), 2)
    
    return soc_voltage

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

# # Callback ketika menerima pesan
# def on_message(client, userdata, msg):
#     try:
#         payload = json.loads(msg.payload.decode())  # Parsing JSON
#         print(f"Pesan diterima dari {msg.topic}:")
#         print(f"Payload: {msg.payload}")

#         DEVICE_ID = payload.get("device_id", "Unknown")
#         DEVICE_TYPE = payload.get("device_type", "Unknown")
#         LOCATION = payload.get("location", "Unknown")
#         # TIMESTAMP = payload.get("timestamp", "Unknown")
#         now = datetime.now()
#         formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
#         TIMESTAMP = formatted_time
#         TEMPERATURE = payload.get("data", {}).get("temperature", "N/A")
#         HUMIDITY = payload.get("data", {}).get("humidity", "N/A")
#         VOLTAGE = payload.get("Battery_status", {}).get("voltage", "N/A")
#         CURRENT = payload.get("Battery_status", {}).get("current", "N/A")
#         POWER = payload.get("Battery_status", {}).get("power", "N/A")
#         # BATTERY = payload.get("battery_level", "N/A")
#         BATTERY = estimate_battery_capacity(VOLTAGE,CURRENT)
        
#         # Format pesan agar lebih rapi dalam bentuk kolom
#         formatted_data = (
#             f"📡 *Device Info* 📡\n"
#             f"──────────────────────\n"
#             f"📌 *Device ID*   : {DEVICE_ID}\n"
#             f"🔎 *Device Type* : {DEVICE_TYPE}\n"
#             f"📍 *Location*    : {LOCATION}\n"
#             f"⏳ *Timestamp*   : {TIMESTAMP}\n"
#             f"──────────────────────\n"
#             f"🌡️ *Temperature* : {TEMPERATURE}°C\n"
#             f"💦 *Humidity*    : {HUMIDITY}%\n"
#             f"⚡ *Voltage*     : {VOLTAGE}V\n"
#             f"⚡ *Current*     : {CURRENT}mA\n"
#             f"🔌 *Power*       : {POWER}mW\n"
#             f"🔋 *Battery*     : {BATTERY}%\n"
#             f"──────────────────────"
#         )

#         send_to_whatsapp(formatted_data)
#     except json.JSONDecodeError:
#         print(f"Pesan tidak valid: {msg.payload.decode()}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        print(f"Pesan diterima dari {msg.topic}:")
        print(f"Payload CSV: {payload_str}")

        data = payload_str.split(",")
        if len(data) < 16:
            raise ValueError("Format CSV tidak lengkap")

        DEVICE_ID       = data[0]
        DEVICE_TYPE     = data[1]
        LOCATION        = data[2]
        TIMESTAMP_DATE       = data[3]  # Pakai timestamp dari device
        TIMESTAMP_TIME       = data[4]  # Pakai timestamp dari device
        TEMPERATURE     = data[5]
        HUMIDITY        = data[6]
        SOLAR_VOLTAGE   = float(data[7])
        SOLAR_CURRENT   = float(data[8])
        SOLAR_POWER     = float(data[9])
        BATTERY_VOLTAGE = float(data[10])
        BATTERY_CURRENT = float(data[11])
        BATTERY_POWER   = float(data[12])
        LOAD_VOLTAGE    = float(data[13])
        LOAD_CURRENT    = float(data[14])
        LOAD_POWER      = float(data[15])
        WATER_TEMP      = float(data[16])
        FLOW_RATE      = float(data[17])

        # Estimasi kapasitas baterai
        BATTERY = estimate_battery_capacity(BATTERY_VOLTAGE, BATTERY_CURRENT)

        # Format pesan WhatsApp
        formatted_data = (
            f"📡 *Device Info* 📡\n"
            f"──────────────────────\n"
            f"📌 *Device ID*   : {DEVICE_ID}\n"
            f"🔎 *Device Type* : {DEVICE_TYPE}\n"
            f"📍 *Location*    : {LOCATION}\n"
            f"⏳ *Timestamp*   : {TIMESTAMP_DATE} {TIMESTAMP_TIME}\n"
            f"──────────────────────\n"
            f"🌡️ *Temperature* : {TEMPERATURE}°C\n"
            f"💦 *Humidity*    : {HUMIDITY}%\n"
            f"☀️ *Solar*       : {SOLAR_VOLTAGE}V / {SOLAR_CURRENT}mA / {SOLAR_POWER}mW\n"
            f"🔋 *Battery*     : {BATTERY_VOLTAGE}V / {BATTERY_CURRENT}mA / {BATTERY_POWER}mW ({BATTERY}%)\n"
            f"🔌 *Load*        : {LOAD_VOLTAGE}V / {LOAD_CURRENT}mA / {LOAD_POWER}mW\n"
            f"🌊 *Water Temp*  : {WATER_TEMP}°C\n"
            f"🌀 *Flow Rate*   : {FLOW_RATE}L/min\n"
            f"──────────────────────"
        )

        send_to_whatsapp(formatted_data)

    except Exception as e:
        print(f"❌ Gagal parsing pesan CSV: {e}")
        print(f"Payload: {msg.payload.decode()}")


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
