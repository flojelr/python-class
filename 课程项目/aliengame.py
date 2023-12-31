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
from star import Star
from pause import Pause

from random import randint

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
        self.stars=pygame.sprite.Group()
        
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)
        
        self.pause=Pause(self)
        
        #创建外星人队伍
        self._creat_fleet()
        self._creat_star()
        
        self.game_active=False  #游戏开始状态
        self.paused = False     #游戏是否暂停
        
        self.play_button = Button(self,"Play",1)
        self.pause_button = Button(self,"Pause or Continue",2)

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
        
        # 判断是否处于暂停状态
        if self.paused == False:
            #背景颜色
            self.screen.fill(self.settings.bg_color) 
            
            #绘制星星
            self.stars.draw(self.screen)
            
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
            
            #绘制暂停按键
            self.pause_button.draw_button()
            
        #刷新窗口
        pygame.display.flip() 
    
    #更新子弹
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.right >= self.screen.get_rect().right:
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
                #左右
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right =True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left =True
                #上下
                elif event.key == pygame.K_UP:
                    self.ship.moving_up =True
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down =True
                
                elif  event.key == pygame.K_q:
                    sys.exit()#退出游戏
                elif event.key == pygame.K_SPACE: #空格
                    self._fire_bullet() #添加一个新子弹
                
                #游戏暂停与继续
                elif event.key == pygame.K_p:
                    if self.paused:
                        # 游戏继续
                        self.paused = False
                    else:
                        # 游戏暂停
                        self.paused = True
                        while(self.paused):
                            self.pause.show_pause()  #显示暂停按键
                            self._check_events()
                            self._check_click_pause() #鼠标点击暂停按键事件检测
                            pygame.display.flip() 
                
                
            elif event.type == pygame.KEYUP:#按键松开
                #左右
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right =False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left =False
                #上下
                elif event.key == pygame.K_UP:
                    self.ship.moving_up =False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down =False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:#鼠标事件检测
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_pause_button(mouse_pos)
    
    #pause按键鼠标事件检测
    def _check_click_pause(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_pause_button(mouse_pos)
    
    #添加一个新子弹
    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullet_allowed:  #判断子弹数量是否超出限制
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    #创建外星人队伍
    def _creat_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        
        current_x,current_y=2*alien_width+80,alien_height+40
        while current_y < (self.settings.screen_height-alien_height):
            while current_x < (self.settings.screen_width-alien_width):
                self._create_alien(current_x,current_y)
                current_x+=3*alien_width
            
            current_y+=3*alien_height
            current_x=2*alien_width+80
    
    #创建一个外星人
    def _create_alien(self,x_position,y_position):
        new_alien=Alien(self)
        new_alien.y=y_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien)
    
    #检测外星人是否到底屏幕底部
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direcition() #改变外星人移动方向并且向左移动
                break
    
    #改变外星人移动方向并且向左移动
    def _change_fleet_direcition(self):
        for alien in self.aliens.sprites():
            alien.rect.x-=self.settings.fleet_drop_speed
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
            if alien.rect.left <= self.screen.get_rect().left:
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
    
    #检测Pause按键是否被鼠标点击
    def _check_pause_button(self,mouse_pos):
        button_clicked = self.pause_button.rect.collidepoint(mouse_pos)
        if button_clicked :
            if self.paused:
                # 游戏继续
                self.paused = False
            else:
                # 游戏暂停
                self.paused = True
                while(self.paused):
                    self.pause.show_pause()
                    self._check_events()
                    self._check_click_pause()
                    pygame.display.flip() 
    
    #创建一片星星
    def _creat_star(self):
        star =Star(self)
        star_width,star_height=star.rect.size
        x=[]
        y=[]
        
        for i in range(0,50):
            x1=randint(0,60)
            y1=randint(0,60)
            while x1 in x:
                x1=randint(0,60)
            while y1 in y:
                y1=randint(0,60)
            x.append(x1)
            y.append(y1)
        for i in range(0,50):
            current_x,current_y=star_width*x[i],star_height*y[i]
            while current_x>self.settings.screen_width:
                current_x=current_x/randint(2,3)
            while current_y>self.settings.screen_height:
                current_y=current_y/randint(2,4)
            self._create_star(current_x,current_y)

    #创建一个星星
    def _create_star(self,x_position,y_position):
        new_star=Star(self)
        new_star.x=x_position
        new_star.rect.x=x_position
        new_star.rect.y=y_position
        self.stars.add(new_star)

if __name__ == "__main__":  
    ai = AlienInvasion()  
    ai.run_game()