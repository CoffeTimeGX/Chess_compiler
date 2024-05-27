import pygame
from board import newBoard
from Pieces import *
from copy import deepcopy


class Game:
    def __init__(self, Width, Height, Rows, Cols, Square,Win):
        self.Win = Win
        self.Board = newBoard(Width, Height, Rows, Cols,Square, Win)
        self.Square = Square
        self.selected = None
        self.turn = White
        self.valid_moves = []
        self.Black_pieces_left = 16
        self.White_pieces_left = 16
        self.roque = False

    def update_window(self):

        self.Board.draw_Board()
        #Board.draw_test()
        self.Board.draw_pieces()
        self.draw_available_moves()
        pygame.display.update()

    def reset(self):
        self.Board = newBoard(Width, Height, Rows, Cols,Square, Win)
        self.Square = Square
        self.selected = None

    def check_game(self):
        if self.checkmate(self.Board):
            if self.turn == White:
                print("Black Wins")
                return True
            else:
                print("White wins")
                return True
    
    def promotion(self,row,col,promotion):
        self.Board.Board[row][col] = 0
        #piece = self.Board.get_piece(row,col)
        self.Board.promote(row,col,promotion, self.turn)
        self.change_turn()


    def enemies_moves(self,piece, Board):
        enemies_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color != piece.color:
                        moves = Board[r][c].get_available_moves(r,c,Board)
                        #print(self.Board.Board[r][c].type, moves)
                        for move in moves:
                            enemies_moves.append(move)
        #print("enemies_moves",enemies_moves)
        return enemies_moves

    def get_King_pos(self,Board):
        for r in range(len(Board)):
            for c in range(len(Board)):
                if Board[r][c] != 0:
                    if Board[r][c].type == "King" and Board[r][c].color == self.turn:
                        return (r,c)

    def simulate_move(self, piece,row,col):
        piece_row, piece_col = piece.row, piece.col
        save_piece = self.Board.Board[row][col]
        if self.Board.Board[row][col] != 0:
            self.Board.Board[row][col] = 0

        self.Board.Board[piece.row][piece.col], self.Board.Board[row][col] = self.Board.Board[row][col], self.Board.Board[piece.row][piece.col]

        king_pos = self.get_King_pos(self.Board.Board)
        if king_pos in self.enemies_moves(piece,self.Board.Board):
            piece.row,piece.col = piece_row, piece_col
            self.Board.Board[piece_row][piece_col] = piece
            self.Board.Board[row][col] = save_piece
            return False

        piece.row,piece.col = piece_row, piece_col
        self.Board.Board[piece_row][piece_col] = piece
        self.Board.Board[row][col] = save_piece
        return True

    def possible_moves(self,Board):
        possible_moves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].color == self.turn and Board[r][c].type != "King":
                        moves = Board[r][c].get_available_moves(r,c,Board)
                        #print(self.Board.Board[r][c].type, moves)
                        for move in moves:
                            possible_moves.append(move)

        return possible_moves


    def checkmate(self,Board):

        king_pos = self.get_King_pos(Board.Board)
        get_king = Board.get_piece(king_pos[0], king_pos[1])
        king_available_moves = set(get_king.get_available_moves(king_pos[0], king_pos[1], Board.Board))
        enemies_moves_set = set(self.enemies_moves(get_king,Board.Board))
        king_moves = king_available_moves - enemies_moves_set
        set1 = king_available_moves.intersection(enemies_moves_set)
        possible_moves_to_def = set1.intersection(self.possible_moves(Board.Board))
        if len(king_moves) == 0 and len(king_available_moves) != 0 and possible_moves_to_def == 0:
            return True

        return False


    def change_turn(self):
        self.roque = False
        if self.turn == White:
            self.turn = Black
        else:
            self.turn = White



    def select(self,row,col):
        
        if self.selected:
            move = self._move(row,col)

            if not move:
                #print("in not move")
                self.selected = None
                self.select(row,col)

        piece = self.Board.get_piece(row,col)
        if piece != 0 and self.turn == piece.color:
            self.selected = piece

            #print(piece)
            self.valid_moves = piece.get_available_moves(row,col,self.Board.Board)
            print("-------------------------------------")
            print("Mouvements autorisés:", self.convert_moves(self.valid_moves))

    def convert_moves(self,moves):
        output = []
        for move in moves:
            y = (     8 if move[0] == 0
                    else 7 if move[0] == 1
                    else 6 if move[0] == 2
                    else 5 if move[0] == 3
                    else 4 if move[0] == 4
                    else 3 if move[0] == 5
                    else 2 if move[0] == 6
                    else 1)
            x = (     'a' if move[1] == 0
                    else 'b' if move[1] == 1
                    else 'c' if move[1] == 2
                    else 'd' if move[1] == 3
                    else 'e' if move[1] == 4
                    else 'f' if move[1] == 5
                    else 'g' if move[1] == 6
                    else 'h')
            output.append(f"{str(x)}{y}")
        return output

    

    def _move(self,row,col):
        piece = self.Board.get_piece(row,col)
        if self.selected and (row,col) in self.valid_moves:
            if piece == 0 or piece.color != self.selected.color:
                if self.simulate_move(self.selected,row,col):

                    self.remove(self.Board.Board,piece,row,col)
                    self.Board.move(self.selected,row,col)
                    if not self.roque:
                        self.change_turn()
                    self.valid_moves = []
                    self.selected = None


                    return True
                return False

        return False


    def remove(self,board,piece,row,col):
        if piece != 0:
            board[row][col] = 0
            if piece.color == White:
                self.White_pieces_left -= 1
            else:
                self.Black_pieces_left -= 1
        print("Pièces blanches restantes : ", self.White_pieces_left)
        print("Pièces  noires  restantes : ", self.Black_pieces_left)


    def draw_available_moves(self):
        if len(self.valid_moves) > 0:
            for pos in self.valid_moves:
                row,col = pos[0],pos[1]
                pygame.draw.circle(self.Win, Green, (col*self.Square + self.Square//2, row*self.Square + self.Square//2),self.Square//8)

    def get_board(self):
        return self.board
