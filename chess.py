import socket
import threading 
import sys

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)



    def handler(self,c,a):
        global connections
        while True:
            data = c.recv(1024)
            print("Data received")
            for connection in self.connections:
                connection.send(bytes(data))
            if not data:
                connections.remove(c)
                c.close()
                break
    def run(self):
        player_doubles = []
        
        while True:    #Main Server Loop, receives two players, creates thread to handle them playing
        
            print("Waiting for player 1:")
            connection1, address1 = self.sock.accept()
            player1 = (connection1, address1)
            print("Player 1 connected;")
            
            print("Waiting for player 2:")
            connection2, address2 = self.sock.accept()
            player2 = (connection2, address2)
            pd = (player1[1],player2[1])
            player_doubles.append(pd)
            print("Player 2 conected;")
            
            print("Starting Game-thread")
            gThread = threading.Thread(target=self.handler, args=(connection1,address1))
            gThread.daemon = True
            gThread.start()
            self.connections.append(connection1)
            print(self.connections)
            print("")            

    


    
class Client:
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   def sendMsg(self):
        while True:
            user_input = input()
            self.sock.send(bytes(user_input))
        
   def __init__(self, address):
        self.sock.connect((address, 10000))
        iThread = threading.Thread(target = self.sendMsg)
        iThread.daemon = True
        iThread.start()
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(data)
       
if(len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()