from pygame.constants import *
import pygame
from character import Character


class Player(Character):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 3, pygame.image.load("art\survivor-idle_shotgun_0.png"))