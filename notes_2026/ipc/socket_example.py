import time, multiprocessing, socket


HOST = "127.0.0.1"
PORT = 5000


def child_process():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"[server] listening port {PORT} ...\n")

        while True:
            conn, addr = sock.accept()
            print("[server] connected from", addr)

            with conn:
                data = conn.recv(1024)
                print("[server] received:", data.decode())
                conn.sendall(b"Hello from server")


# parent process
if __name__ == "__main__":

    p = multiprocessing.Process(target=child_process)
    p.start()

    time.sleep(5)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(b"Hello from client")
        data = sock.recv(1024)
        print("[client] received:", data.decode())

    time.sleep(5)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(b"Hello from client 2")
        data = sock.recv(1024)
        print("[client] received:", data.decode())

    p.terminate()
