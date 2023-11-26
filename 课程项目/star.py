import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self,al_game):
        super().__init__()
        
        super().__init__()
        self.screen=al_game.screen
        # self.settings=al_game.settings
        
        self.image=pygame.image.load('课程项目/star.bmp')
        self.rect=self.image.get_rect()
        
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
        self.x = float(self.rect.x)
