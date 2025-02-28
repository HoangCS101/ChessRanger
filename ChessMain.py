import pygame as p
import time
import PuzzleEngine as ChessEngine
import ChessSearch
import sys

p.init()

WIDTH, HEIGHT = 800, 600
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Select Algorithm")

font = p.font.SysFont('Arial', 40, True)
clock = p.time.Clock()

MAIN_COLOR = (118, 148, 85)
DARK_GREEN = (98, 128, 65)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_background():
    for y in range(HEIGHT):
        color = (
            MAIN_COLOR[0] - y // 10,
            MAIN_COLOR[1] - y // 10,
            MAIN_COLOR[2] - y // 10
        )
        p.draw.line(screen, color, (0, y), (WIDTH, y))

class Button:
    def __init__(self, text, x, y, w, h, color, hover_color):
        self.text = text
        self.rect = p.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        p.draw.rect(screen, color, self.rect, border_radius=10)
        label = font.render(self.text, True, WHITE)
        screen.blit(label, (self.rect.x + 20, self.rect.y + 10))

    def is_clicked(self, event):
        return event.type == p.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

dfs_button = Button("ChessDFS", 270, 250, 260, 60, DARK_GREEN, MAIN_COLOR)
astar_button = Button("ChessAStar", 270, 350, 260, 60, DARK_GREEN, MAIN_COLOR)

def select_algorithm():
    selected_algorithm = None
    while selected_algorithm is None:
        mouse_pos = p.mouse.get_pos()
        screen.fill(WHITE)
        draw_background()

        label = font.render("Select Algorithm", True, WHITE)
        screen.blit(label, (270, 150))

        dfs_button.draw(screen, mouse_pos)
        astar_button.draw(screen, mouse_pos)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            if dfs_button.is_clicked(event):
                selected_algorithm = "DFS"
            if astar_button.is_clicked(event):
                selected_algorithm = "AStar"
        
        p.display.flip()
        clock.tick(30)

    return selected_algorithm

algorithm = select_algorithm()


# Chess board settings
board_width = board_height = 680
dimension = 8  # 8x8 chess board
sq_size = board_height // dimension  # Size of each square on the board
max_fps = 15
images = {}
colours = [p.Color('#EBEBD0'), p.Color('#769455')]  # Board colours

# Move log settings
move_log_panel_width = 210
move_log_panel_height = board_height


def load_images():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP',
              'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP']
    for piece in pieces:
        images[piece] = p.transform.smoothscale(p.image.load(f'images/{piece}.png'), (sq_size, sq_size))

def animate_auto_moves(screen, move_log_font, game_state, move_history):
    for i, move in enumerate(move_history):
        print(f"Step {i+1}: {move}")
        game_state.make_move(move)
        draw_game_state(screen, game_state, (), move_log_font)
        time.sleep(1) # 1 second delay
        p.display.flip()

def get_size(obj, seen=None):
    """ Recursively find the size of objects. """
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(get_size(v, seen) for v in obj.values())
        size += sum(get_size(k, seen) for k in obj.keys())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(get_size(i, seen) for i in obj)
    return size

def main():
    
    screen = p.display.set_mode((board_width + move_log_panel_width, board_height))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    move_log_font = p.font.SysFont('Arial', 14, False, False)

    game_state = ChessEngine.GameState()
    
    if algorithm == "DFS":
        explorer = ChessSearch.ChessDFS(game_state)
    else:
        explorer = ChessSearch.ChessAStar(game_state)
    
    start_time = time.time()
    explorer.explore()
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Print all possible board states explored
    for i, state in enumerate(explorer.get_explored_states()):
        print(f"State {i + 1}:")
        
        # Print every board state to terminal
        for row in state:
            print(row)
        print()
        
        # Check states with only one piece left
        pieces = []
        for row in state[0]:
            for square in row:
                if square != '--':
                    pieces.append(square)
        if len(pieces) == 1:
            move_history = state[1]

    # Measure space used by explored states
    memory_usage = get_size(explorer.get_explored_states())
    print(f"Memory Usage: {memory_usage / (1024 * 1024):.4f} MB")
    print(f"Execution Time: {execution_time:.4f} seconds")
    load_images()
    running = True

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.KEYDOWN:
                if event.key == p.K_SPACE: # Don't hit it twice!!!
                    animate_auto_moves(screen, move_log_font, game_state, move_history)
        
        draw_game_state(screen, game_state, (), move_log_font)
        clock.tick(max_fps)
        p.display.flip()


def draw_game_state(screen, game_state, square_selected, move_log_font):
    """Responsible for all graphics within a current game state"""
    draw_board(screen)  # Draws squares on the board
    highlight_squares(screen, game_state, square_selected)  # Adds highlighting
    draw_pieces(screen, game_state.board)  # Draws pieces on the board
    draw_move_log(screen, game_state, move_log_font)  # Draws the move log


def draw_board(screen):
    """Draw squares on the board using a chess.com colouring pattern"""
    for row in range(dimension):
        for column in range(dimension):
            colour = colours[((row + column) % 2)]
            p.draw.rect(screen, colour, p.Rect(column * sq_size, row * sq_size, sq_size, sq_size))


def highlight_squares(screen, game_state, square_selected):
    """Highlights square selected and last move made"""
    # Highlights selected square
    if square_selected != ():
        row, column = square_selected
        if game_state.board[row][column][0] == 'w':  # Only white pieces can be selected
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(70)  # Transperancy value; 0 transparent; 255 opaque
            s.fill(p.Color('yellow'))
            screen.blit(s, (column * sq_size, row * sq_size))

    # Highlights last move
    if len(game_state.move_log) != 0:
        last_move = game_state.move_log[-1]
        start_row, start_column = last_move.start_row, last_move.start_column
        end_row, end_column = last_move.end_row, last_move.end_column
        s = p.Surface((sq_size, sq_size))
        s.set_alpha(70)
        s.fill(p.Color('yellow'))
        screen.blit(s, (start_column * sq_size, start_row * sq_size))
        screen.blit(s, (end_column * sq_size, end_row * sq_size))


def draw_pieces(screen, board):
    """Draws pieces on the board using the current GameState.board"""
    for row in range(dimension):
        for column in range(dimension):
            piece = board[row][column]
            if piece != '--':  # Add pieces if not an empty square
                screen.blit(images[piece], p.Rect(column * sq_size, row * sq_size, sq_size, sq_size))


def draw_move_log(screen, game_state, font):
    """Draws move log to the right of the screen"""
    move_log_area = p.Rect(board_width, 0, move_log_panel_width, move_log_panel_height)
    p.draw.rect(screen, p.Color('#2d2d2e'), move_log_area)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = f'{i // 2 + 1}. {str(move_log[i])} '
        if i + 1 < len(move_log):  # Makes sure black has made a move
            move_string += f'{str(move_log[i + 1])} '
        move_texts.append(move_string)

    move_per_row = 2
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), move_per_row):
        text = ''
        for j in range(move_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        text_object = font.render(text, True, p.Color('whitesmoke'))
        text_location = move_log_area.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def animate_move(move, screen, board, clock):
    """Animates a move"""
    delta_row = move.end_row - move.start_row  # Change in row
    delta_column = move.end_column - move.start_column  # Change in column
    frames_per_square = 5  # Controls animation speed (frames to move one square)
    frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square

    for frame in range(frame_count + 1):  # Need +1 to complete the entire animation

        #  Frame/frame_count indicates how far along the action is
        row, column = (move.start_row + delta_row*frame/frame_count, move.start_column + delta_column*frame/frame_count)

        # Draw board and pieces for each frame of the animation
        draw_board(screen)
        draw_pieces(screen, board)

        # Erases the piece from its ending square
        colour = colours[(move.end_row + move.end_column) % 2]
        end_square = p.Rect(move.end_column * sq_size, move.end_row * sq_size, sq_size, sq_size)
        p.draw.rect(screen, colour, end_square)

        # Draws a captured piece onto the rectangle if a piece is captured
        if move.piece_captured != '--':
            if move.is_en_passant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_column * sq_size, en_passant_row * sq_size, sq_size, sq_size)
            screen.blit(images[move.piece_captured], end_square)

        # Draws moving piece
        screen.blit(images[move.piece_moved], p.Rect(column * sq_size, row * sq_size, sq_size, sq_size))

        p.display.flip()
        clock.tick(60)  # Controls fame rate per second for the animation


def draw_endgame_text(screen, text):
    font = p.font.SysFont('Helvetica', 32, True, False)
    text_object = font.render(text, True, p.Color('gray'), p.Color('mintcream'))
    text_location = p.Rect(0, 0, board_width, board_height).move(board_width/2 - text_object.get_width()/2,
                                                                 board_height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)

    # Creates a shadowing effect
    text_object = font.render(text, True, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


if __name__ == '__main__':
    main()