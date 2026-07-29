import os
import requests

url = "http://localhost:8888/v1/generation/text-to-image"

# Параметри генерації (можна налаштовувати під себе)
PAYLOAD = {
    "prompt": "Cute fluffy cat playing with a red ball, cinematic lighting",
    "negative_prompt": "low quality, blurry",
    "style_selections": ["Fooocus V2", "Fooocus Cinematic"],
    "performance_selection": "Speed",  # Або "Quality", "Extreme Speed"
    "aspect_ratios_selection": "1024*1024",
    "image_number": 1,
    "output_format": "png"
}

print("Надсилаю запит на генерацію...")
response = requests.post(url, json=PAYLOAD, timeout=300)

if response.status_code != 200:
    print(f"Помилка: {response.status_code}")
    print(response.text)
    exit(1)

# Залежно від налаштувань API повертає або масив посилань, або base64-рядки
result = response.json()
print("Генерація успішна!")

url = result[0]["url"]
print(f"Вивантаження згенерованого зображення за URL: {url}")

image = requests.get(url).content
output_file = os.path.join(f"./{url.rpartition('/')[-1]}")
with open(output_file, "wb") as f:
    f.write(image)

print(f"[+] Дані зображення збережено у файл: {output_file}")
