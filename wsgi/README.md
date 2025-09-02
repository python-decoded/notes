
# Запускаємо gunicorn
Windows підтримує gunicorn лише через WSL

```shell

wsl install

# У WSL терміналі:
sudo apt update
sudo apt install python3 python3-pip python3.12-venv
python3 -m venv .venv
source .venv/bin/activate
pip install gunicorn
python -m gunicorn --worker-class sync -w 3 -b 0.0.0.0:5000 simple_wsgi_app:wsgi_app

```

# Запускаємо waitress

```shell
pip install waitress
waitress-serve --listen=0.0.0.0:5000 'simple_wsgi_app:wsgi_app'
```

# Запускаємо uvicorn

```shell
pip install uvicorn
uvicorn simple_asgi_app:asgi_app --reload --host 0.0.0.0 --port 5000

```

# Запускаємо uvicorn + gunicorn
Windows підтримує gunicorn лише через WSL

```shell
pip install uvicorn gunicorn
python -m gunicorn --worker-class uvicorn.workers.UvicornWorker -w 3 -b 0.0.0.0:5000 simple_asgi_app:asgi_app

```
