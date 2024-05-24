import os

from abstract_syntax import (
    Program, Color, Move, Position, Event, Semicolon, Endgame)
from lexer import Lexer
from paarser import Parser


class Visitor:

    def visit(self, ast, args=None):
        #print(ast.accept(self, args))
        return ast.accept(self, args)
    
    def __init__(self) -> None:
        self.pretty_code = ""
        self.pretty_line = ""
        self.color = ""
        self.move = ""
        self.position = ""
        self.events = []
        self.semicolon = ""
        self.endgame = ""

class PrettyPrinter(Visitor):

    def visitProgram(self, program: Program, args):
        #print(([self.visit(move) for move in program.moves]))
        for object_ in program.game_list:
            for color in program.colors:
                if color == object_:
                    self.visit(color)
                    program.colors.remove(color)
            for move in program.moves:
                if move == object_:
                    self.visit(move)
                    program.moves.remove(move)
            for position in program.positions:
                if position == object_:
                    self.visit(position)
                    program.positions.remove(position)
            for event in program.events:
                if event == object_:
                    self.visit(event)
                    program.events.remove(event)
            for semicolon in program.semicolons:
                if len(program.semicolons) == 1:  #Le dernier point virgule est celui de l'endgame
                    break
                if semicolon == object_:
                    self.visit(semicolon)
                    program.semicolons.remove(semicolon)
            if self.semicolon == ";": #On utilise le point virgule en tant que flag lorsqu'on a fini d'analyser la ligne
                self.pretty_line = (
                    f"{('B: ' if str(self.color).lower()[0] == 'b' else 'N: ')}"
                    f"{str(self.move).capitalize()} "
                    f"{' '*(11 - len(str(self.move)))+'-->  ' +self.position}"
                    f"{''.join(self.events[i] for i in range(len(self.events)))}"
                    f"{self.semicolon}"
                )
                self.pretty_code = f"{self.pretty_code}\n{self.pretty_line}"
                for i in range(len(self.events)): #On efface tous les évenements
                    self.events.pop(0)
            self.semicolon = ""
            
        self.visit(program.endgame)
        for semicolon in program.semicolons:
            if semicolon == object_:
                self.visit(semicolon)
                program.semicolons.remove(semicolon)
        self.pretty_code = (f"{self.pretty_code}\n{str(self.endgame).capitalize()}{self.semicolon}")[1:]
        

    def visitColor(self, color : Color, args):
        self.color = color.value.value

    def visitMove(self, move : Move, args):
        self.move = move.value.value
    
    def visitPosition(self, position : Position, args):
        self.position = position.value.value

    def visitEvent(self, event : Event, args):
        self.events.append(event.value.value)
    
    def visitSemicolon(self, semicolon : Semicolon, args):
        self.semicolon = semicolon.value.value
    
    def visitEndgame(self, endgame : Endgame, args):
        self.endgame = endgame.value.value

if __name__ == '__main__':
    lexer = Lexer()
    lexems = lexer.lex_file("games/mat du berger.txt")
    parser = Parser(lexems)
    program = parser.parse()
    visitor = PrettyPrinter()
    program.accept(visitor)
    print(visitor.pretty_code)