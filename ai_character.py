from pygame.constants import *
from character import Character
import random

class AICharacter(Character):
    def __init__(self, x, y, speed, inertia_size, image):
        super(AICharacter, self).__init__(x, y, speed, image)
        self._curr_intertia = 0
        self._curr_key = None
        self._INERTIA_SIZE = inertia_size

    def get_next_move(self):
        if self._curr_intertia > 0:
            self._curr_intertia -= 1
            return self._curr_key
        self._curr_key = random.choice([K_UP, K_DOWN, K_RIGHT, K_LEFT])
        self._curr_intertia = self._INERTIA_SIZE
        return self._curr_key


    def reset_inertia(self):
        self._curr_intertia = 0      
