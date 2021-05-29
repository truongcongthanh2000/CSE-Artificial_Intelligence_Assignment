import random
from boardState import BoardState

TEACHER = -1
ME = 1

class Player:
    def __init__(self, str_name = "me"):
        if str_name == "me":
            self.player = 1 # Me
        else:
            self.plyer = -1 # Teacher
        self.preBoard = BoardState()
    
    def __str__(self):
        return self.name

    def evaluate(self):
class Storage: 
    def __init__(self) -> None:
        pass
        
class Minimax:
    def __init__(self, board):
        self.board
        pass
    
    def evaluate(self, board):
        pass

class Player_minimax:
    def __init__(self, str_name = "me"):
        self.name = str_name
        self.preBoard = BoardState()
    
    def __str__(self):
        return self.name

    def evaluate(self):
            
