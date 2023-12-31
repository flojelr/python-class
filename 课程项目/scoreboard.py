import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    def __init__(self,al_game):
        self.al_game=al_game
        self.screen=al_game.screen 
        self.screen_rect = self.screen.get_rect()
        self.settings=al_game.settings 
        self.stats=al_game.stats
        
        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,48)
        self.prep_score()
        
        self.prep_high_score()
        
        self.prep_level()
        
        self.prep_ships()
    
    #显示得分
    def prep_score(self):
        rounded_score=round(self.stats.score,-1) #精确到小数点后几位
        score_str="score:"+f"{rounded_score:,}"
        self.score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20
    
    #将得分、等级、最高分、飞船剩余数量放入屏幕
    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.leve_image,self.level_rect)
        
        self.ships.draw(self.screen)
    
    #显示最高分
    def prep_high_score(self):
        with open('课程项目/test.txt', 'w', encoding='utf-8') as f:
            f.write(str(self.stats.high_score))
        high_score=round(self.stats.high_score,-1)
        high_score_str="high score:"+f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    #检查是否是最高分
    def check_high_score(self):
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score 
            self.prep_high_score()
    
    #显示等级
    def prep_level(self):
        level_str="level:"+str(self.stats.level)
        self.leve_image=self.font.render(level_str,True,self.text_color,self.settings.bg_color)
        
        self.level_rect=self.leve_image.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.score_rect.bottom+10
    
    #显示飞船剩余数量
    def prep_ships(self):
        self.ships=Group()
        for ship_number in range(self.stats.ships_left):
            ship=Ship(self.al_game)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)