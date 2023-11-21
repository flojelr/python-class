class Settings:
    def __init__(self):
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230,230,230)
        
        self.ship_limit=0
        
        #子弹
        self.bullet_speed=2.0
        self.bullet_width=50
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        
        self.bullet_allowed=100 #限制屏幕上字典数量
        
        self.alien_speed=1.0
        self.fleet_drop_speed=10
        self.fleet_direction=1 #1向右移动，-1向左移动