import math

from pygame.constants import *
import pygame

from ai_character import AICharacter
import random

class Monster(AICharacter):

    def __init__(self, x, y, speed=3, inertia_size=20):
        super(Monster, self).__init__(x, y, speed=speed, inertia_size=inertia_size, image=pygame.image.load("art\minotaur.png"))