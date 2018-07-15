class Match:
    """ Match class describes a chess game between 2 players. """

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.board = [0]*8
        self.buildBoard()

    def printBoard(self):
        for i in range(8):
            for j in range(8):
                print("|",self.board[i][j],"|")

    def buildBoard(self):

        self.board = [['   '] * 8] * 8

        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.board[7] = [p + '_w' for p in pieces]
        self.board[0] = [p + '_b' for p in pieces]

        self.board[1] = ['p_b'] * 8
        self.board[6] = ['p_w'] * 8
