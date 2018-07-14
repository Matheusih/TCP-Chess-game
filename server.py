import socket
import threading
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
        a = chessMatch.p1.address
        c = chessMatch.p2.connection
        self.players
        while True:
            data = c.recv(1024)
            print("Data received")
            for connection in self.players:
                connection.send(bytes(data))
            if not data:
                self.players.remove(c)
                c.close()
                break

    def close(self):
        # Close the socket
        self.sock.close()
