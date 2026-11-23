from collections import deque
from game.directions import Direction, next_cell
from random import sample

class Arena():
    def __init__(self, width, height, walls):
        self.width = width
        self.height = height
        self.walls = set(walls)

    def is_inside(self, cell):
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, cell):
        return cell in self.walls

    def reachable_cells(self, initial_cell, set_cell_blocked=None):
        if set_cell_blocked is None:
            set_cell_blocked = set()
        queue = deque([initial_cell])
        set_visited = set([initial_cell])
        while queue:
            current_cell = queue.popleft()
            for direction in Direction:
                neighbor_cell = next_cell(current_cell, direction)
                if (self.is_inside(neighbor_cell) 
                    and not self.is_wall(neighbor_cell) 
                    and neighbor_cell not in set_visited 
                    and neighbor_cell not in set_cell_blocked):
                    set_visited.add(neighbor_cell)
                    queue.append(neighbor_cell)
        return set_visited

def start_positions(width, height):
    start_cell_for_human = (2, height // 2)
    start_cell_for_ai = (width - 3, height // 2)
    return start_cell_for_human, start_cell_for_ai

def generate_arena(width, height, density, max_attempts=1000):
    if (width < 10 or height < 10):
        raise ValueError("Width and height must be at least 10.")

    if not (0.15 <= density <= 0.25):
        raise ValueError("Density must be between 15% and 25%")

    start_cell_for_human, start_cell_for_ai = start_positions(width, height)

    neighbor_cells_for_human = set()
    neighbor_cells_for_ai = set()

    for direction in Direction:
        neighbor_cells_for_human.add(next_cell(start_cell_for_human, direction))
        neighbor_cells_for_ai.add(next_cell(start_cell_for_ai, direction))

    list_cells_arena_candidates = list()
    for x in range(width):
        for y in range(height):
            if (
                (x, y) not in neighbor_cells_for_human 
                and (x, y) not in neighbor_cells_for_ai
                and (x, y) != start_cell_for_human
                and (x, y) != start_cell_for_ai
            ):
                list_cells_arena_candidates.append((x,y))

    nb_walls = round(width * height * density)
    for _ in range(max_attempts):
        list_walls = sample(list_cells_arena_candidates, k = nb_walls)
        arena = Arena(height=height, width=width, walls=list_walls)
        if start_cell_for_ai in arena.reachable_cells(start_cell_for_human):
            return arena
    raise RuntimeError(f"Failed to generate a valid arena after {max_attempts} attempts.")