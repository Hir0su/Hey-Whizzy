import requests

user_input = "what is the name of the school"
response = requests.get('http://localhost:5000/raspi_fetch', params={'user_input': user_input.lower()})
print(response)

if response.status_code == 200:
    reply = response.text
    print(reply)
else:
    print("Error:", response.status_code)