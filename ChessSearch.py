import copy

class ChessDFS:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.visited_states = []  # Store visited board states

    def dfs(self, game_state, depth=0, move_history=None):
        """ Recursively explores all possible moves from the current game state. """
        if move_history is None:
            move_history = []  # Initialize move history for the root state

        # Store the current board state along with move history
        self.visited_states.append((copy.deepcopy(game_state.board), move_history.copy()))

        # Get all valid moves from the current state
        valid_moves = game_state.get_valid_moves()

        # If no valid moves left, return (base case)
        if not valid_moves:
            return

        # Explore each move recursively
        for move in valid_moves:
            new_state = copy.deepcopy(game_state)  # Copy the state
            new_move_history = move_history + [move]  # Append move to history
            new_state.make_move(move)  # Apply the move

            self.dfs(new_state, depth + 1, new_move_history)  # Recursive call

    def explore(self):
        """ Start DFS from the initial state """
        self.dfs(self.initial_state)

    def get_explored_states(self):
        """ Return all visited states with their move history """
        return self.visited_states