from lexer import Lexer
from paarser import Parser
from abstract_syntax import AstNode
from rules import LEXEM_RULES   
from visitor import PrettyPrinter
from chess.chess_main import *

class Compiler():
    def __init__(self):
        self.source_file = ""
        self.output_token = False
        self.output_pretty = False
        self.output_start_game = False

    def compile(self, filename):
        lexer = Lexer()
        lexems = lexer.lex_file(filename)
        parser = Parser(lexems)
        program = parser.parse()
        visitor = PrettyPrinter()
        program.accept(visitor)
        if self.output_pretty:
            print(visitor.pretty_code)
            with open("pretty.txt", "w") as f:
                f.write(visitor.pretty_code)
        if self.output_token:
            print("Tokens:\n")
            print(lexems)
        if self.output_start_game:
            main(lexems)
