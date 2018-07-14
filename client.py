import socket
import threading
from arguments import get_args

class Client:
    def __init__(self):
        self.args = get_args()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.args.host, self.args.port))
        iThread = threading.Thread(target = self.sendMsg)
        iThread.daemon = True
        iThread.start()
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(data)

    def sendMsg(self):
         while True:
             user_input = input()
             self.sock.send(bytes(user_input))
