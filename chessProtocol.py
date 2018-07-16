class ChessProtocol(dict):
    def __init__(self, cmd, obj):
        dict.__init__(self)
        self.cmd = cmd
        self.object = obj
