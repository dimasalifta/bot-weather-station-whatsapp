import requests

url = "https://api.greenapi.com/waInstance7103191495/sendMessage/1b176603c8304f2fac6e55871242c73835c693d2618a4a80a2"

payload = {
"chatId": "6289669791324@c.us", 
"message": "test"
}
headers = {
'Content-Type': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)

print(response.text.encode('utf8'))