import socket
import threading
import pickle
from match import Match
from arguments import get_args
from sunfish import *


class Client:
    def __init__(self):
        self.args = get_args()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.match = Match()
        self.searcher = Searcher()
        self.side = 'B'

    def run(self):
        self.sock.connect((self.args.host, self.args.port))

        while True:    #Client Main Loop
            # Game things
            
            data = self.s_recv(1024, "B")
            
                
            if not data:
                break


            if self.match.board.score <= -MATE_LOWER:
                print("You lost")
                break

            if self.match.board.score <= -MATE_LOWER:
                print("You won")
                break

            # Fire up the engine to look for a move.
            move, score = self.searcher.search(self.match.board, secs=2)

            if score == MATE_UPPER:
                print("Checkmate!")


    def s_recv(self, size, expected_type):    #Received messages handler
    
        try:
            msg = self.sock.recv(size)
            data = pickle.loads(msg)
        except EOFError:
            print("Your opponent has timed out! GG!!")
            return 0
            

        if(data[0] == "B"):    #receives board from server
            self.match.upgradeBoard(data[1:])
            print_pos(self.match.board)
            return 1
            
        elif(data[0] == "Y"):   #its your turn, make a move
            # We query the user until she enters a (pseudo) legal move.
            self.side = data[1]
            move = None
            while move not in self.match.board.gen_moves():
                print(self.side+' ',end='')
                match = re.match('([a-h][1-8])'*2, input('Make a move: '))
                if match:
                    move = parse(match.group(1)), parse(match.group(2))
                else:
                    # Inform the user when invalid input (e.g. "help") is entered
                    print("Please enter a move like g8f6")

            self.match.board = self.match.board.move(move)
            
            #if self.side == "W":
            print_pos(self.match.board.rotate())    #Updates the board and rotate so player sees his move
            #else:
            #print_pos(self.match.board)
                
            try:
                self.sock.send(pickle.dumps(move))
            except ConnectionAbortedError:
                print("Server has aborted connection with you :( ")

            return 1
            
        elif(data[0] == "U"):   #Update the board
            # Update the client with adversary (pseudo) legal move.
            move = data[1:]
            self.match.board = self.match.board.move(move[0])
            if self.side == "B":
                print("Your opponent move: ", render(move[0][0]) + render(move[0][1]))
                print_pos(self.match.board)    #Updates the board and rotate so player sees his move
            else:
                print("Your opponent move: ", render(119-move[0][0]) + render(119-move[0][1]))
                print_pos(self.match.board)


            return 1

    def printBoard(self, board):
        board.printBoard()
