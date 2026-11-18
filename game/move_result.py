from enum import Enum

class MoveResult(Enum):
    REFUSED = -1
    VALID = 0
    FATAL = 1