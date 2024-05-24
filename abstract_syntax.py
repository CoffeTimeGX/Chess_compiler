from typing import List

class AstNode:
    def accept(self, visitor, args=None):
        name = self.__class__.__name__
        getattr(visitor, f"visit{name}")(self,args)

class Program(AstNode):
    def __init__(self, colors, moves, positions, events, semicolons, endgame,game_list) -> None:
        self.colors: List[Color] = colors
        self.moves: List[Move] = moves
        self.positions: List[Position] = positions
        self.events: List[Event] = events
        self.semicolons: List[Semicolon] = semicolons
        self.endgame = endgame
        self.game_list = game_list

class Color(AstNode):
    def __init__(self, value: str) -> None:
        self.value: str = value

class Move(AstNode):
    def __init__(self, value: str) -> None:
        self.value: str = value

class Position(AstNode):
    def __init__(self, value: str) -> None:
        self.value: str = value

class Event(AstNode):
    def __init__(self, value: str) -> None:
        self.value: str = value

class Semicolon(AstNode):
    def __init__(self, value: str) -> None:
        self.value: str = value

class Endgame(AstNode):
    def __init__(self, value: str) -> None:
        self.value: str = value