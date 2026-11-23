from game.directions import Direction

class HumanPlayer:
    DIRECTIONS = {
        "z": Direction.UP,
        "q": Direction.LEFT,
        "s": Direction.DOWN,
        "d": Direction.RIGHT
    }

    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id

    def choose_direction(self, game):
        while True:
            answer = input(f"Player {self.name},\nPlease choose a direction (z=up, s=down, q=left, d=right) : ")
            if not answer:
                print("Aucune réponse fournie. Veuillez recommencer.")
                continue
            direction = self.DIRECTIONS.get(answer.strip().lower())
            if direction is not None:
                return direction

            print("Direction invalide. Veuillez recommencer.")