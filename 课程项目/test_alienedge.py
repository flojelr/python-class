import unittest  
import pygame  
from pygame import sprite  
from alien import Alien  # 引入Alien类  
from settings import Settings

class TestAlien(unittest.TestCase):  
    def setUp(self):  
        pygame.init()  
        self.screen = pygame.display.set_mode((800, 600))  
        self.settings=Settings()
        self.alien = Alien(self)  

    def test_check_edges(self):  
        # 检查最开始时外星人是否在屏幕顶部或底部边缘  
        self.assertEqual(self.alien.check_edges(), False)  

    def tearDown(self):  
        pygame.quit()  

if __name__ == '__main__':  
    unittest.main()