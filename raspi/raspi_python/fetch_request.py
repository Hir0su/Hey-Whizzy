import requests

def post_command(command):
    user_input = command
    print(user_input)
    response = requests.get('http://192.168.0.2:5000/raspi_fetch', params={'user_input': user_input.lower()})
    print(response)

    if response.status_code == 200:
        reply = response.text
        print(reply)
        return reply
    else:
        print("Error:", response.status_code)