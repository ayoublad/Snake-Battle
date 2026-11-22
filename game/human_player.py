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
            answer = input(f"Joueur {self.name},\nveuillez choisir une direction (z=haut, s=bas, q=gauche, d=droite) : ")
            if not answer:
                print("Aucune réponse fournie. Veuillez recommencer.")
                continue
            direction = self.DIRECTIONS.get(answer.strip().lower())
            if direction is not None:
                return direction

            print("Direction invalide. Veuillez recommencer.")