from pygame.constants import *
import pygame
from character import Character
import random

class AICharacter(Character):
   
    def get_next_move(self):
        raise NotImplementedError
