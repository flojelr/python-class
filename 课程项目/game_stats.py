import os
class GameStats:
    def __init__(self,al_game):
        self.settings=al_game.settings
        self.reset_stats()
        
        file = "课程项目/test.txt"
        if os.path.exists(file):
            with open('课程项目/test.txt', 'r', encoding='utf-8') as f:
                a=f.read()
            self.high_score=int(a)
        else:
            self.high_score=0
        
        self.level=1
    
    #初始飞船数和分数
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit #初始化飞船剩余数量
        self.score = 0  #初始化得分