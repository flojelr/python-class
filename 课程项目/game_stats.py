class GameStats:
    def __init__(self,al_game):
        self.settings=al_game.settings
        self.reset_stats()
    
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit