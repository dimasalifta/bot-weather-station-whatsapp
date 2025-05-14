import requests
import os
from dotenv import load_dotenv

URL_API_GREENAPI = os.getenv("URL_API_GREENAPI", None)
WHATSAPP_CHAT_ID = os.getenv("WHATSAPP_CHAT_ID", None)
WHATSAPP_GROUP_ID = os.getenv("WHATSAPP_GROUP_ID", None)

# url = "https://api.greenapi.com/waInstance7105242912/sendMessage/7ab1c9ec3fc448b280300ab4eab6d12e149762adb6ec43949c"
url = URL_API_GREENAPI

payload = {
"chatId": "120363416927198799@g.us", 
"message": "test"
}
headers = {
'Content-Type': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)

print(response.text.encode('utf8'))