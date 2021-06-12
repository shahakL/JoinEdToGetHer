import math

from pygame.constants import *

from ai_character import AICharacter
import random

class Monster(AICharacter):

    def __init__(self, x, y, image):
        super(Monster, self).__init__(x, y, 1, image)
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
        self.acceleration = 3
    
    def get_next_move(self):
        rand = random.random()*2*math.pi
        self.ax += math.cos(rand) * self.acceleration
        self.ay += math.sin(rand) * self.acceleration
        self.vx += self.ax
        self.vy += self.ay
        norm = (self.vx**2+self.vy**2)**0.5
        self.vx = self.vx/norm
        self.vy = self.vy/norm
        angle = math.atan2(self.vx,-self.vy)
        pi4 = math.pi/4
        direction = [K_UP, K_LEFT, K_DOWN, K_RIGHT][int(((int(angle / pi4) - 1) % 8) / 2)]
        return direction
