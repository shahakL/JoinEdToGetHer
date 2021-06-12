from pygame.constants import *
import pygame

from ai_character import AICharacter
import random
import time

class FireFly(AICharacter):
    def __init__(self, x, y, speed, light):
        super(FireFly, self).__init__(x, y, speed, pygame.image.load("art/firefly.png"))
        self._init_light = light
        self._light = light
        self._init_time = time.time()
        self._curr_intertia = 0
        self._curr_key = None
    
    def get_next_move(self):
        self._update_light()
        INERTIA_SIZE = 20
        if self._curr_intertia > 0:
            self._curr_intertia -= 1
            return self._curr_key
        self._curr_key = random.choice([K_UP, K_DOWN, K_RIGHT, K_LEFT])
        self._curr_intertia = INERTIA_SIZE

    def _update_light(self):
        dt = time.time() - self._init_time
        if dt > 10:
            self._light = int(self._init_light/2)
        if dt > 20:
            self._light = int(self._init_light/4)
        if dt > 30:
            self._light = 0      

    @property
    def light(self):
        return self._light
