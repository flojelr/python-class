import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,al_game):
        super().__init__()
        self.screen=al_game.screen
        self.settings=al_game.settings
        
        self.image=pygame.image.load('课程项目/alien.bmp')
        self.rect=self.image.get_rect()
        
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
        self.y = float(self.rect.y)
    
    #更新位置
    def update(self):
        self.y+=self.settings.alien_speed*self.settings.fleet_direction
        self.rect.y=self.y
    
    #检查是否到边缘
    def check_edges(self):
        screen_rect=self.screen.get_rect()
        return (self.rect.top<=screen_rect.top)or(self.rect.bottom>=screen_rect.bottom)