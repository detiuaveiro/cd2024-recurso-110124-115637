"""Message Broker"""
import socket
import selectors

class Broker:

    def __init__(self) -> None:
        """inicializar o Broker"""
        self._host = ""
        self._port = 5000

        # start socker
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self._host, self._port))
        self.sock.listen(50)

        # start selector
        self.sel = selectors.DefaultSelector()
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)


    def accept(self, sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)


    def read(self, conn, mask):
        data = conn.recv(1024)
        if data:
            print(data)
            self.sock.send("data received")
        else:
            self.sel.unregister(conn)
            conn.close()

    
    def run(self):
        """Loop indefinetely."""
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

if __name__ == "__main__":
    broker = Broker()
    broker.run()