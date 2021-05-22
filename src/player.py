class Player:
    def __init__(self, game_map):
        self.game_map = game_map
    
    def play(self):
        return {}

    def update(self, data):
        self.game_map.update(data)
