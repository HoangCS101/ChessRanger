import PuzzleLib

class GameState:

    def __init__(self):
        chess_gen = PuzzleLib.ChessBoardGenerator()
        self.board = chess_gen.get_random_board()
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        
    def get_pieces(self):
        pieces = []
        for row in self.board:
            for square in row:
                if square != '--':  # Nếu ô không trống
                    pieces.append(square)
        return pieces

    def make_move(self, move):
        global promoted_piece

        self.board[move.start_row][move.start_column] = '--'  # When a piece is moved, the square it leaves is blank
        self.board[move.end_row][move.end_column] = move.piece_moved  # Moves piece to new location
        self.move_log.append(move)  # Logs move

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_column)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_column)

        # Pawn promotion
        if move.is_pawn_promotion:
            promoted_piece = 'Q'
            self.board[move.end_row][move.end_column] = move.piece_moved[0] + promoted_piece

    def undo_move(self):
        """Undos last move made"""
        if len(self.move_log) != 0:  # Makes sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move  # Switches turn back

            # Updates king positions
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_column)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_column)

            self.checkmate = False
            self.stalemate = False

    def get_valid_moves(self):
        valid_moves = []

        valid_moves = self.get_all_possible_moves()

        # if len(valid_moves) == 0:  # Either checkmate or stalemate
        #     if self.in_check:
        #         self.checkmate = True
        #     else:
        #         self.stalemate = True
        # else:
        #     self.checkmate = False
        #     self.stalemate = False

        return valid_moves

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):  # Number of rows
            for column in range(len(self.board[row])):  # Number of columns in each row
                turn = self.board[row][column][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][column][1]
                    self.move_functions[piece](row, column, moves)  # Calls move function based on piece type
        return moves

    def get_pawn_moves(self, row, column, moves):

        
        move_amount = -1 if self.white_to_move else 1
        back_row = 0 if self.white_to_move else 7

        pawn_promotion = False

        
        if column - 1 >= 0 and self.board[row + move_amount][column - 1] != '--':
            if row + move_amount == back_row:
                pawn_promotion = True
            moves.append(Move((row, column), (row + move_amount, column - 1), self.board, pawn_promotion=pawn_promotion))

        
        if column + 1 < len(self.board) and self.board[row + move_amount][column + 1] != '--':
            if row + move_amount == back_row:
                pawn_promotion = True
            moves.append(Move((row, column), (row + move_amount, column + 1), self.board, pawn_promotion=pawn_promotion))



    def get_rook_moves(self, row, column, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Up, Left, Down, Right

        for d in directions:
            for i in range(1, len(self.board)):
                end_row = row + d[0] * i  
                end_column = column + d[1] * i  

                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):  # Stay on the board
                    if self.board[end_row][end_column] != '--':  # Capture only (must be occupied)
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break  # Stop after capturing
                else:
                    break  # Stop if moving off the board


    def get_knight_moves(self, row, column, moves):
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for d in directions:
            end_row = row + d[0]
            end_column = column + d[1]

            if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):  # Stay on the board
                if self.board[end_row][end_column] != '--':  # Capture only (must be occupied)
                    moves.append(Move((row, column), (end_row, end_column), self.board))


    def get_bishop_moves(self, row, column, moves):
        
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]  # Diagonal directions

        for d in directions:
            for i in range(1, len(self.board)):
                end_row = row + d[0] * i
                end_column = column + d[1] * i

                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):  # Stay on the board
                    if self.board[end_row][end_column] != '--':  # Capture only (must be occupied)
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break  # Stop after the first capture
                else:
                    break  # Stop if moving off the board


    def get_queen_moves(self, row, column, moves):
        self.get_bishop_moves(row, column, moves)
        self.get_rook_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        column_moves = (-1, 0, 1, -1, 1, -1, 0, 1)

        for i in range(8):
            end_row = row + row_moves[i]
            end_column = column + column_moves[i]

            if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board):
                if self.board[end_row][end_column] != '--':
                    moves.append(Move((row, column), (end_row, end_column), self.board))

class Move:
    """
    Class responsible for storing information about particular moves,
    including starting and ending positions, which pieces were moved and captured,
    and special moves such as en passant, pawn promotion, and castling.
    """
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                        'e': 4, 'f': 5, 'g': 6, 'h': 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_square, end_square, board, en_passant=False, pawn_promotion=False, castle=False):
        self.start_row, self.start_column = start_square[0], start_square[1]
        self.end_row, self.end_column = end_square[0], end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.is_pawn_promotion = pawn_promotion

        # En passant
        self.is_en_passant_move = en_passant
        if self.is_en_passant_move:
            self.piece_captured = 'wP' if self.piece_moved == 'bP' else 'bP'

        self.is_castle_move = castle
        self.is_capture = self.piece_captured != '--'
        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        """Overrides the equals method because a Class is used"""
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """Creates a rank and file chess notation"""
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    def get_rank_file(self, rank, column):
        return self.columns_to_files[column] + self.rows_to_ranks[rank]

    def __str__(self):
        """
        Overrides string function to improve chess notation.
        Does not 1) specify checks, 2) checkmate, or 3) when
        multiple same-type pieces can capture the same square.
        """

        end_square = self.get_rank_file(self.end_row, self.end_column)
        
        # Pawn moves
        if self.piece_moved[1] == 'P':
            if self.is_capture and self.is_pawn_promotion:  # Pawn promotion
                return f'{end_square}={promoted_piece}'
            elif self.is_capture and not self.is_pawn_promotion:  # Capture move
                return f'{self.columns_to_files[self.start_column]}x{end_square}'
            else:  # Normal movement
                return end_square

        # Other piece moves
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += 'x'

        return f'{move_string}{end_square}'
