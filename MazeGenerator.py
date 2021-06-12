import random


def find_indices(maze, elem):
    rows = len(maze)
    cols = len(maze[0])
    indices = []
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == elem:
                indices.append((r, c))
    return indices


def print_maze(maze):
    rows = len(maze)
    cols = len(maze[0])
    empty_cells = find_indices(maze, 0)
    ed_her = random.choices(empty_cells, k=2)
    ed = ed_her[0]
    her = ed_her[1]
    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == 0:
                if (row, col) == ed:
                    print('☻', end='')
                elif (row, col) == her:
                    print('☺‍', end='')
                else:
                    print('░░', end='')
            else:
                print('▓▓', end='')
        print()


def neighbours(maze, cell):
    cells = []
    if cell[0] > 0:
        cells.append((cell[0] - 1, cell[1]))
    if cell[0] < len(maze) - 1:
        cells.append((cell[0] + 1, cell[1]))
    if cell[1] > 0:
        cells.append((cell[0], cell[1] - 1))
    if cell[1] < len(maze[0]) - 1:
        cells.append((cell[0], cell[1] + 1))
    if cell[0]<len(maze)-1 and cell[1]<len(maze[0])-1:
        cells.append((cell[0]+1, cell[1]+1))
    if cell[0]<len(maze)-1 and cell[1]>0:
        cells.append((cell[0]+1, cell[1]-1))
    if cell[0]>0 and cell[1]<len(maze[0])-1:
        cells.append((cell[0]-1, cell[1]+1))
    if cell[0]>0 and cell[1]>0:
        cells.append((cell[0]-1, cell[1]-1))
    return cells


def generate_random_maze(rows, cols):
    maze = [[2 for col in range(cols)] for row in range(rows)]
    return regenerate_random_maze(maze)


def regenerate_random_maze(maze):
    rows = len(maze)
    cols = len(maze[0])
    walls_wl = set()
    unvisited_cells = find_indices(maze, 2)
    if not unvisited_cells:
        return maze
    initial_cell = random.choice(unvisited_cells)
    maze[initial_cell[0]][initial_cell[1]] = 0
    walls_wl.update(neighbours(maze, (initial_cell[0], initial_cell[1])))
    while walls_wl:
        current_wall = random.choice(list(walls_wl))
        neighs = neighbours(maze, current_wall)
        wall_neighs = list(filter(lambda neigh: maze[neigh[0]][neigh[1]] == 2, neighs))
        if len(wall_neighs) > 4:
            maze[current_wall[0]][current_wall[1]] = 0
            walls_wl.update(wall_neighs)
        walls_wl.remove(current_wall)

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 2:
                maze[r][c] = 1

    assert all([all([cell in [0, 1] for cell in row]) for row in maze])
    return maze


def main():
    rows = 30
    cols = 100
    maze = generate_random_maze(rows, cols)
    print_maze(maze)


if __name__ == '__main__':
    main()
