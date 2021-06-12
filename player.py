from pygame.constants import *
import pygame


class Player:

    _PLAYER_IMAGE = pygame.image.load("art\survivor-idle_shotgun_0.png")
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._speed = 3
        self._rotated_image = self._PLAYER_IMAGE
 
    def _move_right(self):
        self._x = self._x + self._speed
        self._rotated_image = self._PLAYER_IMAGE
 
    def _move_left(self):
        self._x = self._x - self._speed
        self._rotated_image = pygame.transform.rotate(self._PLAYER_IMAGE, 180)
 
    def _move_up(self):
        self._y = self._y - self._speed
        self._rotated_image = pygame.transform.rotate(self._PLAYER_IMAGE, 90)
         
    def _move_down(self):
        self._y = self._y + self._speed
        self._rotated_image = pygame.transform.rotate(self._PLAYER_IMAGE, -90)

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

    def get_surface(self):
        return self._rotated_image
