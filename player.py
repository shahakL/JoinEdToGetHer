from pygame.constants import *
import pygame

from character import Character
from firefly import FireFly


class Player(Character):

    def __init__(self, x, y, num_fireflies):
        super(Player, self).__init__(x, y, 3, pygame.image.load("art/survivor-idle_shotgun_0.png"))
        self._num_fireflies = num_fireflies

    def action(self, key, app):
        if key is K_SPACE:
            self.create_firefly(app)

    def create_firefly(self, app):
        if self._num_fireflies <= 0:
            return
        self._num_fireflies -= 1
        new_firefly = FireFly(self._x, self._y)
        app.fireflies.append(new_firefly)
