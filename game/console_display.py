class ConsoleDisplay():
    def cell_symbol(self, game, cell):
        if game.snakes[0].head() == cell:
            return "H"
        if game.snakes[0].is_cell_occupied(cell):
            return "h"
        if game.snakes[1].head() == cell:
            return "I"
        if game.snakes[1].is_cell_occupied(cell):
            return "i"
        if game.arena.is_wall(cell):
            return "#"
        return "."

    def render(self, game):
        lignes = []
        for y in range(game.arena.height):
            ligne = ""
            for x in range(game.arena.width):
                ligne += self.cell_symbol(game=game, cell=(x, y))
            lignes.append(ligne)
        return "\n".join(lignes)

    def show_turn(self, game, player):
        print(self.render(game))
        print(f"Turn {game.turn} - It's up to {player.name} to play.\n")

    def show_refused(self, player):
        print(f"Player {player.name} tried to make a u-turn.\n")

    def show_move(self, player, direction):
        print(f"Player {player.name} played direction: {direction.name}\n")

    def show_game_over(self, game, winner):
        print(self.render(game))
        print(f"Game over! Winner: {winner.name}")