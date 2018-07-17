import socket
import threading
import pickle
import json
from chessProtocol import ChessProtocol
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

            chessMatch = Match()
            #player_doubles.append(chessMatch)

            print("Starting Game-thread")
            gThread = threading.Thread(target=self.handler, args=([chessMatch, connection1, connection2]))
            gThread.daemon = True
            gThread.start()
            self.players.append(connection1)
            print(self.players)
            
            

    def handler(self, chessMatch, c1, c2):
        p1c = c1
        p2c = c2
        self.players

        data = pickle.dumps(["B"] + [chessMatch.board.board]) #data serialized
        try:
            p1c.send(data)
            p2c.send(data)
        except:
            print("Player disconnection...")
            return 

        while True:
        
            i = 0
            #Player 1 makes a move
            msg = "YW"
            
            while i < 3:
                print("Sending p1 a message and waiting for his move..")
                p1c.settimeout(30)
                p1c.send(pickle.dumps(msg))
                
                try:
                    move = p1c.recv(1024)  
                    if move:
                        break  
                except:
                    print("P1 Timeout!!! Try again...")
                i += 1
                    
            if ( i >= 3 ):
                print("P1 disconnected!! Ending game thread...")
                p1c.shutdown(socket.SHUT_RDWR)
                p1c.close()
                p2c.close()
                return
            move = pickle.loads(move)
            print("Move received from p1")

            
            msg = pickle.dumps(["U", move])
            p2c.send(msg)
            ########################################

            i = 0
            #Player 2 makes a move
            msg = "YB"
            
            while i < 3:
                print("Sending p2 a message and waiting for his move..")
                p2c.settimeout(30)
                p2c.send(pickle.dumps(msg))
                
                try:
                    move = p2c.recv(1024)
                    if move:
                        break
                except:
                    print("P2 Timeout!!! Try again...")
                    
                i += 1
                    
            if ( i >= 3 ):
                print("P2 disconnected!! Ending game thread...")
                p2c.shutdown(socket.SHUT_RDWR)
                p1c.close()
                p2c.close()
                return
            move = pickle.loads(move)
            print("Move received from p2")

                #chessMatch.updateBoard(move) -- to do
            msg = pickle.dumps(["U", move])
            p1c.send(msg)
            ########################################
