import socket, multiprocessing


HOST = "127.0.0.1"
PORT = 5000


def child_process():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print("[server] listening...")

        while True:
            conn, addr = sock.accept()
            print("[server] connected from", addr)

            with conn:
                data = conn.recv(1024)
                print("[server] received:", data.decode())
                conn.sendall(b"Hello from server")


if __name__ == "__main__":
    p = multiprocessing.Process(target=child_process)
    p.start()
    ...
