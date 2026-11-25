import pygame
from assets.colors import *

class PygameDisplay:
    def __init__(self, width, height, size_cell=40):
        self.width = width
        self.height = height
        self.size_cell = size_cell
        pygame.init()
        self.screen = pygame.display.set_mode(size=(self.width * self.size_cell, self.height * self.size_cell))
        pygame.display.set_caption("Snake Battle")

    def cell_color(self, game, cell):
        if game.snakes[0].head() == cell:
            return LIGHT_GREEN
        if game.snakes[0].is_cell_occupied(cell):
            return DARK_GREEN
        if game.snakes[1].head() == cell:
            return LIGHT_RED
        if game.snakes[1].is_cell_occupied(cell):
            return DARK_RED
        if game.arena.is_wall(cell):
            return BLACK
        return WHITE

    def draw_arena(self, game):
        for y in range(0, self.height):
            for x in range(0, self.width):
                pixel_x = x * self.size_cell
                pixel_y = y * self.size_cell
                cell = (x, y)
                color = self.cell_color(game, cell)
                pygame.draw.rect(self.screen, color, pygame.Rect(pixel_x, pixel_y, self.size_cell, self.size_cell))
        pygame.display.flip()

    def show_turn(self, game, player):
        self.draw_arena(game)
        pygame.display.set_caption(f"Snake Battle - {player.name}'s turn")

    def show_move(self, player, direction):
        pygame.display.set_caption(f"Snake Battle - {player.name} played direction: {direction.name}")

    def show_refused(self, player):
        pygame.display.set_caption(f"Snake Battle - {player.name}'s move was refused")

    def show_game_over(self, game, winner):
        self.draw_arena(game)
        pygame.display.set_caption(f"Snake Battle - {winner.name} wins!")