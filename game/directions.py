from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

def next_cell(cell, direction: Direction):
    """Case voisine de `cell` dans la direction donnée : (x + Δx, y + Δy)."""
    x, y = cell
    dx, dy = direction.value
    return (x + dx, y + dy)