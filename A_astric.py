import heapq

# -----------------------------
# heuristic function
# -----------------------------
def heuristic(board):
    # number of empty cells
    return sum(row.count(0) for row in board)

# -----------------------------
# check if number placement is valid
# -----------------------------
def is_valid(board, row, col, num):
    # check row
    if num in board[row]:
        return False

    # check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    return True

# -----------------------------
# find empty cell
# -----------------------------
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# -----------------------------
# A* sudoku solver
# -----------------------------
def a_star_sudoku(start_board):
    pq = []

    g = 0
    f = g + heuristic(start_board)

    heapq.heappush(pq, (f, g, start_board))

    while pq:
        _, g, board = heapq.heappop(pq)

        empty = find_empty(board)
        if not empty:
            return board  # solved

        row, col = empty

        for num in range(1, 10):
            if is_valid(board, row, col, num):
                new_board = [r[:] for r in board]
                new_board[row][col] = num

                new_g = g + 1
                new_f = new_g + heuristic(new_board)

                heapq.heappush(pq, (new_f, new_g, new_board))

    return None

# -----------------------------
# print sudoku board
# -----------------------------
def print_board(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=" ")
        print()

# -----------------------------
# main
# -----------------------------
if __name__ == "__main__":
    board = [
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

    solution = a_star_sudoku(board)

    if solution:
        print("Solved Sudoku:\n")
        print_board(solution)
    else:
        print("No solution found.")
