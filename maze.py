import random

from MazeGenerator import generate_random_maze, regenerate_random_maze, find_indices


def in_fog(y, x, player, fog_radius):
    return (y - player.position[1]) ** 2 + (x - player.position[0]) ** 2 > fog_radius ** 2


class Maze:
    def __init__(self, rows, cols):
        self.M = rows
        self.N = cols
        self.maze = generate_random_maze(self.M, self.N)
        self.LX = 44
        self.LY = 36

    def draw(self, display_surf, player, fog1_radius, fog2_radius, sprite_wall, sprite_fog1, sprite_fog2, sprite_floor):
        # self.maze = regenerate_random_maze(self.maze)
        for row in range(self.M):
            for col in range(self.N):
                if in_fog(self.LY * row, self.LX * col, player, fog2_radius):
                    display_surf.blit(sprite_fog2, (col * self.LX, row * self.LY))
                    # self.maze[row][col] = 2
                elif in_fog(self.LY * row, self.LX * col, player, fog1_radius):
                    display_surf.blit(sprite_fog1, (col * self.LX, row * self.LY))
                    # self.maze[row][col] = 2
                elif self.maze[row][col] == 1:
                    display_surf.blit(sprite_wall, (col * self.LX, row * self.LY))
                else:
                    display_surf.blit(sprite_floor, (col * self.LX, row * self.LY))

    def check_empty(self, pos):
        x, y = pos
        left_up_pos = (y, x)
        left_down_pos = (y + self.LY - 1, x)
        right_up_pos = (y, x + self.LX - 1)
        right_down_pos = (y + self.LY - 1, x + self.LX - 1)
        positions = [left_up_pos, left_down_pos, right_up_pos, right_down_pos]
        is_floor = [self.is_floor_at(py, px) for (py, px) in positions]
        print((y, x), list(zip(positions, is_floor)))
        return all(is_floor)

    def is_floor_at(self, y, x):
        aligned_y = int(y / self.LY)
        aligned_x = int(x / self.LX)
        return self.maze[aligned_y][aligned_x] == 0

    def random_floor_position(self):
        y, x = random.choice(find_indices(self.maze, 0))
        return y*self.LY, x*self.LX
