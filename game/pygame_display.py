import pygame
from assets.colors import *

class PygameDisplay:
    def __init__(self, width, height, size_cell=40):
        self.width = width
        self.height = height
        self.size_cell = size_cell
        self.info_bar_height = 40
        pygame.init()
        self.screen = pygame.display.set_mode(size=(self.width * self.size_cell, (self.height * self.size_cell) + self.info_bar_height))
        pygame.display.set_caption("Snake Battle")
        #font = pygame.font.Font("assets/fonts/Pricedown Bl.otf", 28)
        font = pygame.font.SysFont("ubuntu", 28)  # Use default font if the custom font is not available
        self.font = font

    def draw_info_bar(self, text):
        pygame.draw.rect(self.screen, LIGHT_GREY, pygame.Rect(0, self.height * self.size_cell, self.width * self.size_cell, self.info_bar_height))
        text_surface = self.font.render(text, True, BLACK)
        self.screen.blit(text_surface, (10, self.height * self.size_cell + 10))
        pygame.display.flip()

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
        self.screen.fill(LIGHT_GREY)
        for y in range(0, self.height):
            for x in range(0, self.width):
                pixel_x = x * self.size_cell
                pixel_y = y * self.size_cell
                cell = (x, y)
                color = self.cell_color(game, cell)
                pygame.draw.rect(self.screen, color, pygame.Rect(pixel_x, pixel_y, self.size_cell - 1, self.size_cell - 1))

    def show_turn(self, game, player):
        self.draw_arena(game)
        self.draw_info_bar(f"Turn: {game.turn} - {player.name}'s turn")

    def show_move(self, player, direction):
        pygame.time.wait(100)  # Wait for 100 milliseconds to show the move
        self.draw_info_bar(f"{player.name} played direction: {direction.name}")

    def show_refused(self, player):
        self.draw_info_bar(f"{player.name}'s move was refused. Please choose a different direction.")

    def show_game_over(self, game, winner):
        self.draw_arena(game)
        text = f"{winner.name} wins!"
        self.draw_info_bar(text)
