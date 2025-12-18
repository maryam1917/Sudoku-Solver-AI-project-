# Sudoku Solver (CSP)
# Constraint Propagation + Search(Backtracking)

rows = 'ABCDEFGHI'
cols = '123456789'
digits = '123456789'

#Creates combinations of row labels and column labels Ex: cross("A", "123") → ["A1", "A2", "A3"]
def cross(a, b):
    return [x + y for x in a for y in b]

#Creates combinations of row labels and column labels Ex: ["A1", "A2", ..., "I9"]  (81 boxes)
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [
    cross(rs, cs)
    for rs in ('ABC', 'DEF', 'GHI')
    for cs in ('123', '456', '789')
]

# Stores all units in one list
unitlist = row_units + column_units + square_units
"""
units["A1"] →
[
  Row A,
  Column 1,
  Top-left square
]

peers["A1"] →
(all boxes in same row, column, or square except A1)

"""
units = {box: [u for u in unitlist if box in u] for box in boxes}
peers = {box: set(sum(units[box], [])) - {box} for box in boxes}

# Convert grid string into a dictionary of possible values
def grid2values(grid):
    values = {}
    for box, char in zip(boxes, grid):
        if char in digits:
            values[box] = char
        else:
            values[box] = digits
    return values


# Display Sudoku grid
def display(values):
    width = 1 + max(len(values[b]) for b in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)

    for r in rows:
        print(
            ''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                    for c in cols)
        )
        if r in 'CF':
            print(line)
    print()

# Constraint Strategies
# Elimination Rule
def eliminate(values):
    solved_boxes = [b for b in boxes if len(values[b]) == 1]

    for box in solved_boxes:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

# Only Choice Rule
def only_choice(values):
    for unit in unitlist:
        for digit in digits:
            places = [box for box in unit if digit in values[box]]
            if len(places) == 1:
                values[places[0]] = digit
    return values

# Naked Twins Rule
def naked_twins(values):
    for unit in unitlist:
        twins = [box for box in unit if len(values[box]) == 2]

        seen = {}
        for box in twins:
            val = values[box]
            seen.setdefault(val, []).append(box)

        for val, boxes_with_val in seen.items():
            if len(boxes_with_val) == 2:
                for box in unit:
                    if box not in boxes_with_val:
                        for digit in val:
                            values[box] = values[box].replace(digit, '')
    return values

# Puzzle Reduction: Apply constraint propagation repeatedly
def reduce_puzzle(values):
    stalled = False

    while not stalled:
        solved_before = len([b for b in boxes if len(values[b]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_after = len([b for b in boxes if len(values[b]) == 1])

        # Stop if no new values were assigned
        stalled = solved_before == solved_after

        # Fail if a box has no possible values
        if any(len(values[b]) == 0 for b in boxes):
            return False

    return values

# Search (Backtracking)
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False

    if all(len(values[b]) == 1 for b in boxes):
        return values
    _, box = min((len(values[b]), b) for b in boxes if len(values[b]) > 1)
    for digit in values[box]:
        new_values = values.copy()
        new_values[box] = digit
        attempt = search(new_values)
        if attempt:
            return attempt

    return False
# Solver
def solve(grid):
    values = grid2values(grid)
    return search(values)
# Example
if __name__ == "__main__":

    puzzle = (
        "53..7...."
        "6..195..."
        ".98....6."
        "8...6...3"
        "4..8.3..1"
        "7...2...6"
        ".6....28."
        "...419..5"
        "....8..79"
    )

    print("Original Sudoku:")
    display(grid2values(puzzle))

    solution = solve(puzzle)

    print("Solved Sudoku:")
    display(solution)
