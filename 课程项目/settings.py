class Settings:
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(20,85,100)
        
        self.ship_limit=3 #飞船剩余数量
        
        #子弹
        self.bullet_width=10
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullet_allowed=100 #限制屏幕上子弹数量
        
        self.fleet_drop_speed=10 #外星人左移幅度
        
        self.speedup_scale=1.1 #飞船、外星人、子弹移动速度的增长速度
        self.score_scale=1.5 #击败外星人分数的增长速度
        
        self.initialize_dynamic_settings()
    
    #初始化飞船、外星人、子弹移动速度
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed=2.5
        self.alien_speed=1.0
        
        self.fleet_direction=1 #1向下移动，-1向上移动
        
        self.alien_points=50    #每个飞船的得分
    
    #增加飞船、外星人、子弹移动速度
    def increase_speed(self):
        self.ship_speed *=self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.alien_speed *=self.speedup_scale
        
        self.alien_points=int(self.alien_points*self.score_scale)