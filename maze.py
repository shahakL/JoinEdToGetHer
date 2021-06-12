import random

import pygame

from MazeGenerator import generate_random_maze, regenerate_random_maze, find_indices


def in_fog(y, x, player, fireflies, fog_radius):
    return all((y - c.position[1]) ** 2 + (x - c.position[0]) ** 2 > fog_radius ** 2 for c in fireflies + [player])


def blit_alpha(source, target, opacity, location):
    tmp = target.copy()
    tmp.convert_alpha()
    tmp.fill((opacity, opacity, opacity), None, pygame.BLEND_RGB_SUB)
    source.blit(tmp, location)


class Maze:
    def __init__(self, rows, cols):
        self.M = rows
        self.N = cols
        self.maze = generate_random_maze(self.M, self.N)
        self.LX = 36
        self.LY = 36

    def draw(self, display_surf, player, fireflies, fog1_radius, fog2_radius, sprite_wall, alpha, sprite_fog, sprite_floor, monsters):
        for row in range(self.M):
            for col in range(self.N):
                if in_fog(self.LY * row, self.LX * col, player, fireflies, fog2_radius):
                    display_surf.blit(sprite_fog, (col * self.LX, row * self.LY))
                elif in_fog(self.LY * row, self.LX * col, player, fireflies, fog1_radius):
                    if self.maze[row][col] == 1:
                        blit_alpha(display_surf, sprite_wall, alpha, (col * self.LX, row * self.LY))
                    else:
                        blit_alpha(display_surf, sprite_floor, alpha, (col * self.LX, row * self.LY))
                else:
                    if self.maze[row][col] == 1:
                        display_surf.blit(sprite_wall, (col * self.LX, row * self.LY))
                    else:
                        display_surf.blit(sprite_floor, (col * self.LX, row * self.LY))

        for monster in monsters:
            is_far = in_fog(monster.position[1], monster.position[0], player, [], fog1_radius)
            isnt_too_far = not in_fog(monster.position[1], monster.position[0], player, [], fog2_radius)
            if is_far:
                if isnt_too_far:
                    blit_alpha(display_surf, monster._IMAGE, alpha, monster.position)
            else:
                display_surf.blit(monster._IMAGE, monster.position)

    def check_empty(self, pos):
        x, y = pos
        left_up_pos = (y, x)
        left_down_pos = (y + self.LY - 10, x)
        right_up_pos = (y, x + self.LX - 10)
        right_down_pos = (y + self.LY - 10, x + self.LX - 10)
        positions = [left_up_pos, left_down_pos, right_up_pos, right_down_pos]
        is_floor = [self.is_floor_at(py, px) for (py, px) in positions]
        return all(is_floor)

    def is_floor_at(self, y, x):
        aligned_y = int(y / self.LY)
        aligned_x = int(x / self.LX)
        is_valid = 0 <= aligned_y < self.M and 0 <= aligned_x < self.N
        return is_valid and self.maze[aligned_y][aligned_x] == 0

    def random_floor_position(self, n=1):
        ps = random.choices(find_indices(self.maze, 0), k=n)
        return [(y * self.LY, x * self.LX) for (y, x) in ps]
