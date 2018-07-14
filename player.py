class Player:
    """ Player class which contains all data necessary for the Server synchronize things """
    # Count the players (for generating unique IDs)
    ids = 0

    def __init__(self, connection, address):
        """Initialize a player with its connection to the server"""
        # Generate a unique id for this player
        Player.ids = Player.ids + 1
        self.id = Player.ids
        # Assign the corresponding connection
        self.connection = connection
        # Assign the corresponding connection
        self.address = address
        # Set the player waiting status to True
        self.is_waiting = True
