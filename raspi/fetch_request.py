import requests
from lxml import html

def post_command(command):
    user_input = command
    print(user_input)
    response = requests.get('http://IP ADDRESS HERE/raspi_fetch', params={'user_input': user_input.lower()})
    print(response)

    if response.status_code == 200:
        reply_html = response.text
        tree = html.fromstring(reply_html)
        image_url = tree.xpath('//img/@src')

        if image_url:
            reply_type = 2
            file_name = image_url[0].split('/')[-1]  # Extract the file name from the URL
            print(reply_html)

            start_tag = "<p>"
            end_tag = "</p>"

            start_index = reply_html.find(start_tag) + len(start_tag)
            end_index = reply_html.find(end_tag, start_index)
            p_text = reply_html[start_index:end_index]
            print(p_text)
            print(file_name)

            return p_text, reply_type, file_name
        else:
            reply_type = 1
            print(reply_html)
            return reply_html, reply_type, None
    else:
        print("Error:", response.status_code)