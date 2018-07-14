import socket
import threading
import pickle
from arguments import get_args

class Client:
    def __init__(self):
        self.args = get_args()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.args.host, self.args.port))

        while True:    #Client Main Loop
            data = self.s_recv(1024, "B")
            if not data:
                break
            print(data)

            
    def s_recv(self, size, expected_type):    #Received messages handler
        msg = self.sock.recv(size)
        data = pickle.loads(msg)
        if(data[0] == "B"):    #receives board from server
            board_content = data[1:]
            self.printBoard(board_content)
            return 1
        elif(data[0] == "Y"):   #its your turn, make a move
            move = input("Make a move: ")  #move format: "22 34" moves piece at (2,2) to (3,4)
            self.sock.send( pickle.dumps(move) )
            return 1
            
            
    def printBoard(self, board):
        for i in range(40):
            print("-", end='')
        print("")
        for i in range(8):
            for j in range(8):
                print("|",str(board[i][j]),"|", end='')
            print("")
        for i in range(40):
            print("-", end='')
