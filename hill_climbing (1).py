import random
import copy

N = 9

# -------------------------------------------------
# Count conflicts (heuristic function)
# -------------------------------------------------
def get_conflicts(grid):
    conflicts = 0

    # Column conflicts
    for col in range(N):
        seen = set()
        for row in range(N):
            val = grid[row][col]
            if val in seen:
                conflicts += 1
            else:
                seen.add(val)

    # 3x3 subgrid conflicts
    for box_row in range(0, N, 3):
        for box_col in range(0, N, 3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    val = grid[box_row + i][box_col + j]
                    if val in seen:
                        conflicts += 1
                    else:
                        seen.add(val)

    return conflicts


# -------------------------------------------------
# Generate initial complete state (rows are valid)
# -------------------------------------------------
def generate_initial_state(grid, fixed):
    new_grid = copy.deepcopy(grid)

    for row in range(N):
        missing = [x for x in range(1, 10) if x not in new_grid[row]]
        random.shuffle(missing)

        for col in range(N):
            if not fixed[row][col]:
                new_grid[row][col] = missing.pop()

    return new_grid


# -------------------------------------------------
# Generate neighbors by swapping inside rows only
# -------------------------------------------------
def get_neighbors(grid, fixed):
    neighbors = []

    for row in range(N):
        free_cells = [c for c in range(N) if not fixed[row][c]]

        for i in range(len(free_cells)):
            for j in range(i + 1, len(free_cells)):
                c1, c2 = free_cells[i], free_cells[j]
                neighbor = copy.deepcopy(grid)
                neighbor[row][c1], neighbor[row][c2] = neighbor[row][c2], neighbor[row][c1]
                neighbors.append(neighbor)

    return neighbors


# -------------------------------------------------
# Hill Climbing Algorithm
# -------------------------------------------------
def hill_climbing_sudoku(grid):
    fixed = [[cell != 0 for cell in row] for row in grid]

    current = generate_initial_state(grid, fixed)
    current_h = get_conflicts(current)

    while current_h > 0:
        neighbors = get_neighbors(current, fixed)
        best_state = current
        best_h = current_h

        for neighbor in neighbors:
            h = get_conflicts(neighbor)
            if h < best_h:
                best_state = neighbor
                best_h = h

        if best_h >= current_h:
            break  # Local optimum reached

        current = best_state
        current_h = best_h

    return current, current_h


# -------------------------------------------------
# INPUT SUDOKU 
# -------------------------------------------------
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# -------------------------------------------------
# RUN SOLVER
# -------------------------------------------------
solution, h = hill_climbing_sudoku(grid)

print("Final heuristic value (conflicts):", h)
print("Final Sudoku State:")
for row in solution:
    print(row)

