from pygame.constants import *
import pygame
from character import Character
import random

class Monster(Character):

    def __init__(self, x, y):
        super(Monster, self).__init__(x, y, pygame.image.load("art\minotaur.png"))
        self._speed = 2
    
    def get_next_move(self):
        prob_do_nothing = 0.95
        if random.random() > prob_do_nothing:
            return random.choice([K_UP, K_DOWN, K_RIGHT, K_LEFT])


