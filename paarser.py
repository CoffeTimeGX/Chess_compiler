import logging 
import rules
logger = logging.getLogger(__name__)
import time

from abstract_syntax import (AstNode, Program, Color, Move, Position, Event, Semicolon, Endgame)

class ParsingException(Exception):
    pass


class Parser:
    def __init__(self, lexems):
        """
        Component in charge of syntaxic analysis
        """
        self.lexems = lexems
        self.ast_root = AstNode()

    def accept(self):
        """
        Pops the lexem out of the lexems list.
        """
        self.show_next()
        return self.lexems.pop(0)
    
    def show_next(self):
        """
        Returns the next token in the list WITHOUT popping it.
        """
        try:
            return self.lexems[0]
        except IndexError:
            ("No more lexems left.")

    def expect(self, many_expectations, tags):
        """
        Pops the next token from the lexems list and tests its type through the tag.
        """
        if not many_expectations:
            next_lexem = self.show_next()
            if next_lexem.tag != tags:
                raise ParsingException(
                    f"ERROR at {str(self.show_next().position)}: Expected {tag}, got {next_lexem.tag} instead"
                )
            return self.accept()
        else:
            next_lexem = self.show_next()
            for tag in tags:
                if next_lexem.tag == tag:
                    return self.accept()
            raise ParsingException(
                f"ERROR at {str(self.show_next().position)}: Excpected {tags}, got {next_lexem.tag} instead"
            )
    
    def remove_comments(self):
        """
        Removes the comments from the token list by testing their tags
        """
        self.lexems = [lexem for lexem in self.lexems if lexem.tag != "COMMENT"]

    def parse(self):
        """
        Main function: launches the parsing operation given a lexem list.
        """
        try:
            self.remove_comments()
            program = self.parse_program()
        except ParsingException as err:
            logger.exception(err)
            raise
        return program

    def parse_program(self):
        """
        Parsing of the lexem list given as an argument when instanciating the class
        It expects the correct order in each string between semi-columns ';'
        """
        #We initialize all the lists of each step of the description of a single move
        colors_list = []
        moves_list = []
        positions_list = []
        events_list = []
        semicolons_list = []
        #This list gathers all the previous lists elements in the order in which they were declared so that we keep track of it
        game_list = []
        
        while self.show_next().tag != "endgame": #Keyword endgame ends the parsing
            #Least amount of code we'll have between each semicolon
            while self.show_next().tag != "semicolon": #As long as the next token isn't a semicolon, we stay in the same move
                if self.show_next().tag == "blanc":
                    white = Color(self.expect(False,"blanc"))
                    colors_list.append(white)
                    game_list.append(white)
                    move = self.parse_white()
                    moves_list.append(move)
                    game_list.append(move)
                    position, events = self.parse_white()
                    positions_list.append(position)
                    game_list.append(position)
                    events_list.extend(events)
                    game_list.extend(events)

                elif self.show_next().tag == "noir":
                    black = Color(self.expect(False,"noir"))
                    colors_list.append(black)
                    game_list.append(black)
                    move = self.parse_black()
                    moves_list.append(move)
                    game_list.append(move)
                    position, events = self.parse_black()
                    positions_list.append(position)
                    game_list.append(position)
                    events_list.extend(events)
                    game_list.extend(events)
            
            #If there isn't a semicolon after that, then it means there's still actions described for this move
            #Then we accept the semicolon
            semicolon = self.parse_semicolon()
            semicolons_list.append(semicolon)
            game_list.append(semicolon)

        endgame = self.parse_endgame()
        game_list.append(endgame)
        semicolon = self.parse_semicolon()
        semicolons_list.append(semicolon)
        game_list.append(semicolon)
        return Program(colors_list, moves_list, positions_list, events_list, semicolons_list, endgame,game_list)

    def parse_white(self):
        """
        Parsing of whites' move
        We return either the first part of the move which is the moving piece,
        Or the second which is the aimed square to which it is moving
        and with different actions(events) optionally
        """
        if self.show_next().tag in ["cavalier","fou","pion","reine","roi","pion","tour"]:
            moving_piece = self.parse_moving_piece()
            return moving_piece
        elif self.show_next().tag == "aimed_square":
            position, events = self.parse_aimed_position()
            return position, events

    def parse_black(self):
        """
        Parsing of blacks' move
        We return either the first part of the move which is the moving piece,
        Or the second which is the aimed square to which it is moving
        and with different actions(events) optionally
        """
        events = []
        if self.show_next().tag in ["cavalier","fou","pion","reine","roi","pion","tour"]:
            moving_piece = self.parse_moving_piece()
            return moving_piece
        elif self.show_next().tag == "aimed_square":
            position, events = self.parse_aimed_position()
            return position, events

    def parse_moving_piece(self):
        """
        Parsing of the moving piece
        """
        move = Move(self.expect(True,["cavalier","fou","pion","reine","roi","pion","tour"]))
        return move

    def parse_aimed_position(self):
        """
        Parsing of the aimed square
        """
        position =  Position(self.expect(False,"aimed_square"))
        events = []
        while self.show_next().tag in ["capture","petit_roque","grand_roque","echec","checkmate","nul","p_reine","p_tour","p_cavalier","p_fou"]:
            events.append(self.parse_event())
        return position, events

    def parse_event(self):
        """
        Parsing of the event of a given move
        """
        event = Event(self.expect(True,["capture","petit_roque","grand_roque","echec","checkmate","nul","p_reine","p_tour","p_cavalier","p_fou"]))
        return event
    
    def parse_semicolon(self):
        """
        Parsing of a semicolon
        """
        semicolon = Semicolon(self.expect(False,"semicolon"))
        return semicolon
    
    def parse_endgame(self):
        """
        Parsing of the 'Endgame' keyword
        """
        endgame = Endgame(self.expect(False,"endgame"))
        return endgame