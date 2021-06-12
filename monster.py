import math

from pygame.constants import *

from ai_character import AICharacter
import random


class Monster(AICharacter):

    def __init__(self, x, y, speed=3, inertia_size=20, image=None):
        super(Monster, self).__init__(x, y, speed=speed, inertia_size=inertia_size, image=image)
