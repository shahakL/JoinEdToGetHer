from pygame.constants import *
import pygame

from ai_character import AICharacter
import random
import time

class FireFly(AICharacter):
    def __init__(self, x, y, speed, inertia_size=40, light=10):
        super(FireFly, self).__init__(x, y, speed, inertia_size, image=pygame.image.load("art/firefly.png"))
        self._init_light = light
        self._light = light
        self._init_time = time.time()
    
    def get_next_move(self):
        next_move = super(FireFly, self).get_next_move()
        self._update_light()
        return next_move


    def _update_light(self):
        dt = time.time() - self._init_time
        if dt > 5:
            self._light = int(self._init_light/2)
        if dt > 8:
            self._light = int(self._init_light/4)
        if dt > 10:
            self._light = 0


    @property
    def light(self):
        return self._light
