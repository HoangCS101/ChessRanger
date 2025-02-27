import copy
import heapq

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

        # Stop if only one piece remains
        if len([piece for row in game_state.board for piece in row if piece != '--']) == 1:
            return

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
    
class ChessAStar:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.visited_states = []  # Store explored states

    def a_star_search(self):
        """ Performs A* search to find the optimal path to a single remaining piece """
        priority_queue = []
        heapq.heappush(priority_queue, (0, 0, self.initial_state, []))  # (cost, depth, state, path)
        visited = set()

        while priority_queue:
            cost, depth, current_state, path = heapq.heappop(priority_queue)
            state_key = tuple(tuple(row) for row in current_state.board)
            # [['--', '--',...],...] -> (('--', '--',...),...)
            # Since list lookups is much less efficient.
            print(state_key)
            if state_key in visited:
                continue
            visited.add(state_key)
            self.visited_states.append((copy.deepcopy(current_state.board), path.copy()))  # Store explored state
            
            if len(current_state.get_pieces()) == 1:
                return path  # Goal reached: one piece left
            
            for move in current_state.get_valid_moves():
                new_state = copy.deepcopy(current_state)
                new_state.make_move(move)
                new_cost = cost + 1
                heuristic_value = chess_ranger_heuristic(new_state)
                heapq.heappush(priority_queue, (new_cost + heuristic_value, len(path), new_state, path + [move]))
        
        return None  # No solution found

    def explore(self):
        """ Start A* search from the initial state """
        return self.a_star_search()

    def get_explored_states(self):
        """ Return all visited states with their move history """
        return self.visited_states

# Adjusted heuristic function for Chess Ranger
def chess_ranger_heuristic(game_state):
    """ Heuristic function for Chess Ranger: Estimates moves needed to reach one piece left """
    return len([piece for row in game_state.board for piece in row if piece != '--']) - 1