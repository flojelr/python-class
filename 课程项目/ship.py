import pygame 
from pygame.sprite import Sprite

class Ship(Sprite):
    
    def __init__(self,al_game):
        super().__init__()
        
        self.screen=al_game.screen
        self.seetings = al_game.settings
        self.screen_rect = al_game.screen.get_rect()
        
        self.image = pygame.image.load('课程项目/ship.bmp')
        self.rect = self.image.get_rect()
        
        self.rect.midleft = self.screen_rect.midleft
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        #移动标志
        self.moving_right = False
        self.moving_left = False  
        
        self.moving_up = False
        self.moving_down = False 
    
    #更新飞船位置
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.seetings.ship_speed
        
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.seetings.ship_speed
        
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.seetings.ship_speed
        
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.seetings.ship_speed
        
        self.rect.x=self.x
        self.rect.y=self.y
    
    def blitme(self):
        #将图片放入窗口
        self.screen.blit(self.image,self.rect)
    
    #将飞船显示在屏幕左边中间
    def center_ship(self):
        self.rect.midleft=self.screen_rect.midleft
        self.x=float(self.rect.x)