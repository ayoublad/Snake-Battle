from collections import deque

class Snake:
    def __init__(self, initial_position):
        self.body = deque([initial_position])

    def head(self):
        return self.body[-1]

    def neck(self):
        if len(self.body) > 1:
            return self.body[-2]
        return None

    def tail(self):
        return self.body[0]

    def is_cell_occupied(self, cell):
        return cell in self.body
    
    def move_forward(self, destination, growth):
        if not growth:
            self.body.popleft()
        self.body.append(destination)
