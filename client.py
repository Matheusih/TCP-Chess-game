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

    def run(self):
        self.sock.connect((self.args.host, self.args.port))

        while True:    #Client Main Loop
            # Game things
            if self.match.board.score <= -MATE_LOWER:
                print("You lost")
                break

            data = self.s_recv(1024, "B")
            if not data:
                break

            print_pos(self.match.board.rotate())

            if self.match.board.score <= -MATE_LOWER:
                print("You won")
                break

            # Fire up the engine to look for a move.
            move, score = self.searcher.search(self.match.board, secs=2)

            if score == MATE_UPPER:
                print("Checkmate!")


    def s_recv(self, size, expected_type):    #Received messages handler
        msg = self.sock.recv(size)
        data = pickle.loads(msg)
        if(data[0] == "B"):    #receives board from server
            self.match.upgradeBoard(data[1:])
            return 1
        elif(data[0] == "Y"):   #its your turn, make a move
            # We query the user until she enters a (pseudo) legal move.
            move = None
            while move not in self.match.board.gen_moves():
                match = re.match('([a-h][1-8])'*2, input('Make a move: '))
                if match:
                    move = parse(match.group(1)), parse(match.group(2))
                else:
                    # Inform the user when invalid input (e.g. "help") is entered
                    print("Please enter a move like g8f6")

            self.match.board = self.match.board.move(move)
            self.sock.send(pickle.dumps(move))

            return 1
        elif(data[0] == "U"):   #Update the board
            # Update the client with adversary (pseudo) legal move.
            move = data[1:]
            print('Your opponent movement: ', move)
            self.match.board = self.match.board.move(move[0])
            return 1

    def printBoard(self, board):
        board.printBoard()
