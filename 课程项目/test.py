import pygame  
import sys
from time import sleep
from settings import Settings
from ship import Ship 
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:  
    def __init__(self):  
        pygame.init()  
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #全屏
        self.settings=Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))#设置窗体大小
        
        pygame.display.set_caption('Alien Invasion')  
        #获取时钟
        self.clock = pygame.time.Clock() 
        
        self.ship = Ship(self)
        
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)
        
        #创建外星人队伍
        self._creat_fleet()
        
        self.game_active=False  #游戏开始状态
        self.play_button = Button(self,"Play")

    def run_game(self):  
        while True:
            
            self._check_events()    #按键事件检测
            
            if self.game_active:
                self.ship.update() 
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()   #更新屏幕
            
            #刷新时间
            self.clock.tick(60)  
    
    #更新屏幕
    def _update_screen(self):
        
        #背景颜色
        self.screen.fill(self.settings.bg_color) 
        
        #绘制子弹
        for bullet in self.bullets.sprites():
                bullet.draw_bullet()
        
        #绘制飞船
        self.ship.blitme() 
        
        #绘制外星人
        self.aliens.draw(self.screen)
        
        #显示得分
        self.sb.show_score()
        
        #绘制play按键
        if not self.game_active:
            self.play_button.draw_button()
        
        #刷新窗口
        pygame.display.flip() 
    
    #更新子弹
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom<=0:
                    self.bullets.remove(bullet)   #删除子弹     
        self._check_bullet_alien_collisions()   #检查子弹与外星人的碰撞
    
    #更新外星人队伍位置
    def _update_aliens(self):
        self._check_fleet_edges() 
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship,self.aliens): #判断外星人与自己飞船是否碰撞
            self._ship_hit()
        
        self._check_aliens_bottom() #检查外星人是否到底屏幕底部
    
    #检查子弹与外星人的碰撞
    def _check_bullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True) #判断是否发生碰撞
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)    #计算分数
            self.sb.prep_score()    #显示得分
            self.sb.check_high_score()  #检查是否是最高分
            
        if not self.aliens:
            self.bullets.empty()    #清空子弹
            self._creat_fleet()     #刷新外星人队伍
            self.settings.increase_speed()  #增加飞船、外星人、子弹移动速度
            
            self.stats.level+=1     #等级+1
            self.sb.prep_level()    #刷新等级显示
    
    #按键事件检测
    def _check_events(self):
        for event in pygame.event.get(): #接受输入
            if event.type==pygame.QUIT:#退出
                exit()
                
            elif event.type == pygame.KEYDOWN:#按键按下
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right =True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left =True
                elif  event.key == pygame.K_q:
                    sys.exit()#退出游戏
                elif event.key == pygame.K_SPACE: #空格
                    self._fire_bullet() #添加一个新子弹
                    
            elif event.type == pygame.KEYUP:#按键松开
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right =False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left =False
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:#鼠标事件检测
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    #添加一个新子弹
    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullet_allowed:  #判断子弹数量是否超出限制
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    #创建外星人队伍
    def _creat_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        
        current_x,current_y=alien_width+80,alien_height+80
        while current_y < (self.settings.screen_height-4*alien_height):
            while current_x < (self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x+=3*alien_width
            
            current_y+=3*alien_height
            current_x=alien_width+80
    
    #创建一个外星人
    def _create_alien(self,x_position,y_position):
        new_alien=Alien(self)
        new_alien.x=x_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien)
    
    #检测外星人是否到底屏幕底部
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direcition() #改变外星人移动方向并且向下移动
    
    #改变外星人移动方向并且向下移动
    def _change_fleet_direcition(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
    
    def _ship_hit(self):
        if self.stats.ships_left>0:
            self.stats.ships_left -= 1
            
            self.sb.prep_ships() #显示剩余飞船
            
            self.bullets.empty()    #清空子弹
            self.aliens.empty()     #清空外星人
            
            self._creat_fleet()     #重新创建外星人队
            self.ship.center_ship() #重新显示飞船在屏幕底部中间
            
            sleep(0.5)  #等待0.5s
        else :
            self.game_active=False  #设置游戏状态的不开始
            pygame.mouse.set_visible(True)  #设置鼠标为不可见状态
    
    #检查外星人是否到底屏幕底部
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
    
    #检测Play按键是否被鼠标点击
    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            
            self.settings.initialize_dynamic_settings() #初始化游戏设置
            
            self.stats.reset_stats()    #初始飞船数和分数
            
            self.sb.prep_score()    #显示分数
            self.sb.prep_level()    #显示等级
            self.sb.prep_ships()    #显示剩余飞船数量
            
            self.game_active=True  
            
            self.bullets.empty()    #清空现有子弹
            self.aliens.empty()     #清空现有外星人
            
            self._creat_fleet()     #创建外星人队
            self.ship.center_ship() #创建飞船
            
            pygame.mouse.set_visible(False) #鼠标不可见

if __name__ == "__main__":  
    ai = AlienInvasion()  
    ai.run_game()