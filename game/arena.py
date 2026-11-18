from collections import deque
from game.directions import DIRECTIONS, next_cell

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
            for direction in DIRECTIONS.values():
                neighbor_cell = next_cell(current_cell, direction)
                if (self.is_inside(neighbor_cell) 
                    and not self.is_wall(neighbor_cell) 
                    and neighbor_cell not in set_visited 
                    and neighbor_cell not in set_cell_blocked):
                    set_visited.add(neighbor_cell)
                    queue.append(neighbor_cell)
        return set_visited