import pygame

class Pause:
    def __init__(self,al_game):
        self.al_game =al_game
        self.screen=al_game.screen 
        self.screen_rect=self.screen.get_rect()
        self.settings=al_game.settings
        
        self.text_color=(30,30,30)
        self.font = pygame.font.Font(None, 90)
        self.show_pause()
    
    def show_pause(self):
        self.pause_text = self.font.render("Game Pasued!!!", True,self.text_color,self.settings.bg_color)
        self.text_rect = self.pause_text.get_rect()
        self.text_rect.center = self.screen_rect.center
        self.screen.blit(self.pause_text, self.text_rect)