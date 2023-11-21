import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,al_game):
        super().__init__()
        self.screen=al_game.screen
        self.settings=al_game.settings
        
        self.image=pygame.image.load('alien/alien.bmp')
        self.rect=self.image.get_rect()
        
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
        self.x = float(self.rect.x)
    
    def update(self):
        self.x+=self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x=self.x
    
    def check_edges(self):
        screen_rect=self.screen.get_rect()
        return (self.rect.right>=screen_rect.right)or(self.rect.left<=0)