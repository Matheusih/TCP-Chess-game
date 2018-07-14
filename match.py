class Match:
    """ Match class describes a chess game between 2 players. """
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.board = [0]*8
        self.buildBoard()
        
    def printBoard(self):
        for i in range(40):
            print("_", end='')
        print("")
        for i in range(8):
            for j in range(8):
                print("|",self.board[i][j],"|", end='')
            print("")

    def buildBoard(self):
        for i in range(8):
            self.board[i] = [0]*8
            
        self.board[0] = ['R','N','B','Q','K','B','N','R']
        self.board[7] = ['R','N','B','Q','K','B','N','R']
        for i in range(8):
            self.board[1][i] = 'p'
            self.board[6][i] = 'p'
        for i in range(2,6):
            self.board[i] = [' ',' ',' ',' ',' ',' ',' ',' ']
