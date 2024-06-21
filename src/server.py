"""Server"""
import socket, selectors


class Server:
    def __init__(self) -> None:
        """Inicializar o servidor"""
        self.broker_host = ""
        self.broker__port = 5000

        # start socker
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        # start selector
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.sock, selectors.EVENT_READ, self.read)


    def connect(self):
        try:
            self.sock.connect((self.broker_host, self.broker__port))
            self.sock.setblocking(False)

            # enviar mensagem de registo para o broker
            self.sock.send(b"register")

        except ConnectionRefusedError:
            print("Connection refused")
        except Exception as e:
            print('Erro:', e)




    def read(self, conn, mask):
        data = conn.recv(1024)
        if data:
            print(data)
        else:
            self.sel.unregister(conn)
            conn.close()

        
    def run(self):
        """Loop indefinetely."""

        self.connect()

        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

if __name__ == "__main__":
    server = Server()
    server.run()