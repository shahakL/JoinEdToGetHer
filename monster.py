import math

from pygame.constants import *

from ai_character import AICharacter
import random


class Monster(AICharacter):

    def __init__(self, x, y, speed=3, inertia_size=20, image=None):
        super(Monster, self).__init__(x, y, speed=speed, inertia_size=inertia_size, image=image)
    
    def get_next_move(self, pos_player):
        vector_to_player = [self._x-pos_player[0], self._y-pos_player[1]]
        dist_to_player = sum(x**2 for x in vector_to_player)**0.5
        if dist_to_player < 100:
            self.reset_inertia()

            prob_list = [0.55, 0.01, 0.33, 0.01]
            cum_prob_list = [sum(prob_list[0:i+1]) for i in range(len(prob_list))]
            keys_ordered = []
            temp_x = []
            temp_y = []

            if vector_to_player[0] > 0:
                temp_x = [K_LEFT, K_RIGHT]
            else:
                temp_x = [K_RIGHT, K_LEFT]
            if vector_to_player[1] > 0:
                temp_y = [K_UP, K_DOWN]
            else:
                temp_y = [K_DOWN, K_UP]

            if abs(vector_to_player[0]) > abs(vector_to_player[1]):
                keys_ordered.extend(temp_x)
                keys_ordered.extend(temp_y)
            else:
                keys_ordered.extend(temp_y)
                keys_ordered.extend(temp_x)
            
            p = random.random()
            if p < cum_prob_list[0]:
                return keys_ordered[0]
            elif p < cum_prob_list[1]:
                return keys_ordered[1]
            elif p < cum_prob_list[2]:
                return keys_ordered[2]
            else:
                return keys_ordered[3]

        else:
            return super().get_next_move()
