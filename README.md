# ChessRanger  

<ins>Rules:</ins>  

Chess Ranger is a logic puzzle with simple rules and challenging solutions.  

The rules are simple:  
- Pieces move as standard chess pieces.  
- You can perform only capture moves.  
- You are allowed to capture the king.  
- The goal is to end up with one single piece on the board.  

<ins>How to use:</ins> 

"py ChessMain.py" to run  

Choose your desired Search Algorithm:  

<p align="center">
  <img src="https://github.com/user-attachments/assets/7951930a-bf0b-49e3-be5b-fc469d76716c" height="400">
</p>

Press SPACE to start auto-solve:  

<p align="center">
  <img src="https://github.com/user-attachments/assets/ba31a10b-1ceb-4747-92ca-383fb0a44100" height="400">
</p>

Check explored states, performance stats and solution steps in terminal  

<p align="center">
  <img src="https://github.com/user-attachments/assets/01d084de-9164-4e41-bd68-3ea076386fd9" height="400">
</p>

<ins>Used Algorithms:</ins>  

DFS:  
- Algorithm-wise, this simply traverses the state search tree using a depth-first search approach.  
- Recursively explores all valid moves from a given game state.  
- Stops when only one piece remains.

A*:  
- Sticks with exploring all valid moves from a given game state, prioritizes states in a priority queue based on cost + heuristic value.
- Heuristic function estimates the number of moves needed to reduce the board to a single remaining piece by counting the number of pieces left (n) and assuming at least (n - 1) moves are required to eliminate them.
- Expands the least-cost state first, avoiding revisits.  
- Stops when only one piece remains.  
