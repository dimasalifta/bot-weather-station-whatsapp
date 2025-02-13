import requests

url = "https://7103.api.greenapi.com/waInstance7103191495/sendMessage/1b176603c8304f2fac6e55871242c73835c693d2618a4a80a2"

payload = {
"chatId": "120363401415006234@g.us", 
"message": "test"
}
headers = {
'Content-Type': 'application/json'
}

response = requests.post(url, json=payload, headers=headers)

print(response.text.encode('utf8'))