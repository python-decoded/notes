# pip install requests
# export API_KEY=...
# export API_TOKEN=...

import os
from requests import Session

API_KEY = os.getenv("API_KEY")
API_TOKEN = os.getenv("API_TOKEN")

upload_image = False
download_image = False

session = Session()
session.headers["Authorization"] = f'OAuth oauth_consumer_key="{API_KEY}", oauth_token="{API_TOKEN}"'

host = "https://api.trello.com"
card_id = "67b1090770b9b1e4a75b9bea"


# Загрузити зображення
if upload_image:
    data = {"name": "some_image.jpeg",
            "setCover": "true"}

    with open("image_small.jpg", "rb") as file:
        file_content = file.read()

    files = {"file": file_content}
    res = session.post(f"{host}/1/cards/{card_id}/attachments", data=data, files=files)
    print(res.status_code)


# Скачати зображення
if download_image:
    res = session.get(f"{host}/1/cards/{card_id}/attachments")
    attachment = res.json()[0]  # за умови, що картка має 1 прикріплену картинку
    url = attachment["url"]

    res = session.get(url)
    content = res.content

    with open("downloaded_file.jpg", "wb") as file:
        file.write(content)
