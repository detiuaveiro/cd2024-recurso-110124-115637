"""Server"""
import socket, selectors
from tasks import generate_possible_puzzles
from sudoku import Sudoku

# class Server:
#     def __init__(self) -> None:
#         """Inicializar o servidor"""
#         self.broker_host = ""
#         self.broker__port = 5000

#         # start socker
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


#         # start selector
#         self.sel = selectors.DefaultSelector()
#         self.sel.register(self.sock, selectors.EVENT_READ, self.read)


#     def connect(self):
#         try:
#             self.sock.connect((self.broker_host, self.broker__port))
#             self.sock.setblocking(False)

#             # enviar mensagem de registo para o broker
#             self.sock.send(b"register")

#         except ConnectionRefusedError:
#             print("Connection refused")
#         except Exception as e:
#             print('Erro:', e)




#     def read(self, conn, mask):
#         data = conn.recv(1024)
#         if data:
#             print(data)
#         else:
#             self.sel.unregister(conn)
#             conn.close()

        
#     def run(self):
#         """Loop indefinetely."""

#         # self.connect()

#         while True:
#             events = self.sel.select()
#             for key, mask in events:
#                 callback = key.data
#                 callback(key.fileobj, mask)

# if __name__ == "__main__":
    # server = Server()
    # server.run()
puzzle =  [
    [4, 2, 6, 5, 7, 1, 8, 9, 0], 
    [1, 9, 8, 4, 0, 3, 7, 5, 6], 
    [3, 5, 7, 8, 9, 6, 2, 1, 0], 
    [9, 6, 2, 3, 4, 8, 1, 7, 5], 
    [7, 0, 5, 6, 1, 9, 3, 2, 8], 
    [8, 1, 3, 7, 5, 0, 6, 4, 9],
    [5, 8, 1, 2, 3, 4, 9, 6, 7], 
    [6, 7, 9, 1, 8, 5, 4, 0, 2], 
    [2, 3, 4, 9, 6, 7, 5, 8, 1]]
pzl = Sudoku(puzzle)
sub_puzzles = pzl.generate_sub_puzzles()
first = sub_puzzles[0]

def handle_puzzle(puzzle):
    tasks_ids = [generate_possible_puzzles.delay(sub_puzzle) for sub_puzzle in puzzle]

    return tasks_ids

