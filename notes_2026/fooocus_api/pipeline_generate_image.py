import os
import time
import requests
from testcontainers.core.container import DockerContainer


def generate_image(prompt, **kwargs):
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, low quality",
        "performance_selection": "Speed",  # Або "Quality", "Extreme Speed"
        "image_number": 1,
        "output_format": "png"
    } | kwargs

    gen_url = f"{base_url}/v1/generation/text-to-image"

    try:
        gen_response = requests.post(gen_url, json=payload, timeout=300)  # Великий таймаут на генерацію
        if gen_response.status_code != 200:
            print(f"Помилка генерації: {gen_response.status_code}")
            print(gen_response.text)
            exit(1)

        result = gen_response.json()
        print("Генерація успішна! Збереження результату...")

        url = result[0]["url"].replace(":8888", f":{host_port}")

        print(f"Вивантаження згенерованого зображення за URL: {url}")
        image = requests.get(url).content
        output_file = os.path.join(current_dir, f"{url.rpartition('/')[-1]}")
        with open(output_file, "wb") as f:
            f.write(image)

        print(f"Дані зображення збережено у файл: {output_file}")

        return output_file

    except Exception as e:
        print(f"Сталася помилка під час запиту: {e}")


def wait_server(base_url):
    # Очікування готовності сервера (Healthcheck)
    # Оскільки Fooocus може завантажувати модель при першому старті, таймаут ставимо великий
    api_ready = False
    for i in range(120):  # Очікуємо до 10 хвилин (якщо треба завантажити JuggernautXL)
        try:
            # Перевіряємо доступність Swagger документації як індикатор готовності
            response = requests.get(f"{base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("[+] API готове до роботи!")
                api_ready = True
                break
        except requests.exceptions.RequestException:
            if i % 6 == 0:  # Виводимо повідомлення кожні 30 секунд
                print(f"Сервер усе ще запускається...")
            time.sleep(5)

    if not api_ready:
        print("Помилка: Сервер не запустився за відведений час.")
        exit(1)


FOOOCUS_MODELS_DIR = os.environ["FOOOCUS_MODELS_DIR"]

models_dir = os.path.join(FOOOCUS_MODELS_DIR)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ініціалізація Testcontainers
# Використовуємо DockerContainer для гнучкого налаштування параметрів
fooocus_container = (
    DockerContainer("konieshadow/fooocus-api")
    .with_name("fooocus_container")
    .with_exposed_ports(8888)
    # Монтуємо локальну папку моделей у контейнер
    .with_volume_mapping(models_dir, "/app/repositories/Fooocus/models", "rw")
    # Передаємо змінні оточення для NVIDIA
    .with_env("NVIDIA_DRIVER_CAPABILITIES", "compute,utility")
    .with_env("NVIDIA_VISIBLE_DEVICES", "all")
)

# Прокидаємо підтримку GPU (аналог --gpus all у Docker CLI)
# Testcontainers під капотом використовує docker-py, де це налаштовується через HostConfig
fooocus_container.with_kwargs(
    device_requests=[{"Driver": "nvidia", "Count": -1, "Capabilities": [["compute", "utility"]]}]
)

print("Запуск контейнера Fooocus API через Testcontainers...")
with fooocus_container as container:
    # Отримуємо динамічний або фіксований порт (Testcontainers зазвичай мапить 8888 на випадковий вільний порт Windows)
    host_ip = container.get_container_host_ip()
    host_port = container.get_exposed_port(8888)
    base_url = f"http://{host_ip}:{host_port}"

    print(f"Контейнер запущено. Очікуємо ініціалізації API на {base_url}...")

    wait_server(base_url)
    generate_image("Red sport car in mountain landscape, photorealistic")
    generate_image("A beautiful cinematic landscape of misty mountains at sunrise, 8k, highly detailed")
    generate_image("Cute fluffy cat playing with a red ball, cinematic lighting")

    print("Вихід із блоку 'with'. Testcontainers автоматично зупиняє та видаляє контейнер...")

print("Контейнер повністю вимкнено та видалено. Роботу завершено.")
