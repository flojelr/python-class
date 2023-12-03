import pygame.font

class Button:
    
    def __init__(self,al_game,msg,flag):
        self.screen = al_game.screen 
        self.screen_rect = self.screen.get_rect()
        
        if flag==1:
            self.width,self.height=200,50
            self.button_color=(90,76,80)
            self.text_color=(255,255,255)
            self.font=pygame.font.SysFont(None,48)
        else:
            self.width,self.height=340,50
            self.button_color=(150,76,20)
            self.text_color=(255,255,255)
            self.font=pygame.font.SysFont(None,48)
        
        self.rect =pygame.Rect(0,0,self.width,self.height)
        if flag==1:
            self.rect.center = self.screen_rect.center
        else:
            self.rect.bottom = self.screen_rect.bottom
            self.rect.left = self.screen_rect.left
        
        self._prep_msg(msg)
    
    #按键显示的设置
    def _prep_msg(self,msg):
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    #将Play按键放入屏幕
    def draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)