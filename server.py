import socket
import threading
import pickle
from match import Match
from player import Player
from arguments import get_args


class Server:
    """ Responsible for all inter game management between games!! """

    def __init__(self):
        self.args = get_args()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []

        # Use a simple lock when matching players
        self.lock_matching = threading.Lock()

        # Reserving server side address #
        self.bind()

    def close(self):
        # Close the socket
        self.sock.close()

    def bind(self):
        self.sock.bind((self.args.host, self.args.port))
        self.sock.listen(1)
        print("Server is fixed to ---> host:", self.args.host, "port:", self.args.port)

    def run(self):
        player_doubles = []

        while True:    # Main Server Loop, receives two players, creates thread to handle them playing

            print("Waiting for player 1:")
            connection1, address1 = self.sock.accept()
            player1 = Player(connection1, address1)
            print("Player 1 connected;")

            print("Waiting for player 2:")
            connection2, address2 = self.sock.accept()
            player2 = Player(connection2, address2)
            print("Player 2 conected;")

            chessMatch = Match(player1, player2)
            player_doubles.append(chessMatch)

            print("Starting Game-thread")
            gThread = threading.Thread(target=self.handler, args=([chessMatch]))
            gThread.daemon = True
            gThread.start()
            self.players.append(connection1)
            print(self.players)

    def handler(self, chessMatch):
        p1c = chessMatch.p1.connection
        p2c = chessMatch.p2.connection
        self.players

        data = pickle.dumps(["B"] + chessMatch.board)
        p1c.send(data)
        p2c.send(data)

        while True:
            #Player 1 makes a move
            msg = "Y"
            p1c.send(pickle.dumps(msg))
            move = p1c.recv(1024)
            move = pickle.loads(move)
            print("Move received from p1")

            #chessMatch.updateBoard(move)  -- to do

            #Player 2 makes a move
            msg = "Y"
            p2c.send(pickle.dumps(msg))
            move = p2c.recv(1024)
            move = pickle.loads(move)
            print("Move received from p2")

            #chessMatch.updateBoard(move) -- to do
