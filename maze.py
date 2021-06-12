from MazeGenerator import generate_random_maze


def in_fog(row, col, player, fog_radius):
    return (row*36-player.position[0])**2+(col*44-player.position[0])**2>fog_radius**2


class Maze:
    def __init__(self, rows, cols):
        self.M = rows
        self.N = cols
        self.maze = generate_random_maze(self.M, self.N)

    def draw(self, display_surf, player, fog_radius, sprite_wall, sprite_fog, sprite_floor):
        for row in range(self.M):
            for col in range(self.N):
                if in_fog(row, col, player, fog_radius):
                    display_surf.blit(sprite_fog, (col*44, row*36))
                elif self.maze[row][col]==1:
                    display_surf.blit(sprite_wall, (col*44, row*36))
                else:
                    display_surf.blit(sprite_floor, (col * 44, row * 36))

    def check_empty(self, pos):
        x, y = pos
        x = int(x/44)
        y = int(y/36)
        return self.maze[x][y] == 0
