from pygame.constants import *
import pygame

from ai_character import AICharacter
import random

class FireFly(AICharacter):
    def __init__(self, x, y, speed, light):
        super(FireFly, self).__init__(x, y, speed, pygame.image.load("art/firefly.png"))
        self._light = light
    
    def get_next_move(self):
        prob_do_nothing = 0.95
        if random.random() > prob_do_nothing:
            return random.choice([K_UP, K_DOWN, K_RIGHT, K_LEFT])
