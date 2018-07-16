from sunfish import *
class Match:
    """ Match class describes a chess game between 2 players. """

    def __init__(self):
        self.buildBoard()
    def printBoard(self):
        print_pos(self.board)

    def buildBoard(self):
        self.board = Position(initial, 0, (True,True), (True,True), 0, 0)

    def upgradeBoard(self, board):
        # It comes as a list unwrap it
        self.board.setBoard(board[0])
