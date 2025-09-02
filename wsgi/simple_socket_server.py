import socket

response = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

{message}
"""


with socket.socket() as s:
    s.bind(('127.0.0.1', 5000))
    s.listen(5)   # чекаємо на під'єднання, максимум 5 під'єднаннь

    while True:
        conn, addr = s.accept()  # встановлення з'єднання

        with conn:
            print('Connected by', addr)
            data = conn.recv(1024).decode("utf-8")  # отримання повідомлення
            print(data)
            if not data:
                break

            # відповідь залежно від урл у запиті
            method, path, protocol = data.splitlines()[0].split(" ")
            if "hello" in path:
                message = "Hi there!!!"
            else:
                message = "Can I help you!!!!"

            conn.sendall(response.format(message=message).encode("utf-8"))
