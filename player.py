from pygame.constants import *


class Player:
    def __init__(self):
        self._x = 44
        self._y = 44
        self._speed = 0.3
 
    def _move_right(self):
        self._x = self._x + self._speed
 
    def _move_left(self):
        self._x = self._x - self._speed
 
    def _move_up(self):
        self._y = self._y - self._speed
 
    def _move_down(self):
        self._y = self._y + self._speed

    @property
    def position(self):
        return [self._x, self._y]

    def check_future_position(self, key):
        future_x = self._x
        future_y = self._y
        if key is K_RIGHT:
            future_x += 1
        elif key is K_LEFT:
            future_x -= 1
        elif key is K_UP:
            future_y -= 1
        elif key is K_DOWN:
            future_y += 1
        return [future_x, future_y]

    def move(self, key):
        key_to_movement = {K_RIGHT: self._move_right,
                           K_LEFT: self._move_left,
                           K_UP: self._move_up,
                           K_DOWN: self._move_down}
        key_to_movement[key]()