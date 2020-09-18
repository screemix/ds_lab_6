import socket
from threading import Thread
import os

HOST = 'localhost'
PORT = 8096


class ClientListener(Thread):
    def __init__(self, sk):
        super().__init__(daemon=True)
        self.sk = sk

    def run(self):
        print(f'Connected at {addr}')
        i = 0

        while True:
            ### receive a piece of data ###
            data = conn.recv(1024)

            ### if it is first one, extract filename and etc ###
            if i == 0:
                metadata = data.decode('utf-8')
                filename = metadata
                # performing actions to distinct between files with same names #
                if filename in os.listdir():
                    same_files_list = [s for s in os.listdir() if filename.split('.')[0] + '_copy' in s]
                    name_list = filename.split('.')
                    if len(same_files_list) != 0:
                        num = len(same_files_list) + 1
                        filename = name_list[0] + f'_copy_{str(num)}.' + name_list[1]
                    else:
                        filename = name_list[0] + '_copy_1.' + name_list[1]
                f = open(f'{filename}', 'wb')
                i += 1
                conn.sendall(b'ok')
            else:
                f.write(data)
            if not data:
                break
        f.close()


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        ClientListener(conn).start()
