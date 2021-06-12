import math

from pygame.constants import *

from ai_character import AICharacter
import random


class Princess(AICharacter):

    def __init__(self, x, y, image):
        super(Princess, self).__init__(x, y, speed=0.2, inertia_size=10, image=image)
