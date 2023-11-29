import unittest  
import pytest
import pygame
from aliengame import AlienInvasion

class Test_alien(unittest.TestCase):
    def setUp(self):
        pygame.init()
    
    def tearDown(self):
        pygame.quit()
    
    def test_gameClass(self):
        self.assertEqual(AlienInvasion().settings.screen_width,1200)
        self.assertEqual(AlienInvasion().settings.screen_height,800)
    
    def test_play(self):
        x=AlienInvasion()