from collections import deque
import copy

# Sudoku input from the image
initial_board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def bfs_sudoku_solver(board):
    queue = deque()
    queue.append(board)

    while queue:
        current = queue.popleft()
        empty = find_empty(current)

        if not empty:
            return current  # Solution found

        row, col = empty

        for num in range(1, 10):
            if is_valid(current, row, col, num):
                new_board = copy.deepcopy(current)
                new_board[row][col] = num
                queue.append(new_board)

    return None

# Solve the Sudoku
solution = bfs_sudoku_solver(initial_board)

# Print solution
for row in solution:
    print(row)