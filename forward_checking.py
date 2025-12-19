N = 9
VALUES = set(range(1, 10))

def print_grid(grid):
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(grid[i][j], end=" ")
        print()
    print()


def is_complete(grid):
    return all(all(cell != 0 for cell in row) for row in grid)


def neighbors(r, c):
    nbrs = set()
    for i in range(N):
        nbrs.add((r, i))
        nbrs.add((i, c))
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            nbrs.add((i, j))
    nbrs.remove((r, c))
    return nbrs


def prune(domains, r, c, val):
    for (nr, nc) in neighbors(r, c):
        domains[(nr, nc)].discard(val)

def init_domains(grid):
    domains = {}
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 0:
                domains[(r, c)] = VALUES.copy()
            else:
                domains[(r, c)] = {grid[r][c]}

    # Initial constraint propagation
    for r in range(N):
        for c in range(N):
            if grid[r][c] != 0:
                prune(domains, r, c, grid[r][c])

    return domains


def forward_check(domains, r, c, val):
    removed = []
    for (nr, nc) in neighbors(r, c):
        if val in domains[(nr, nc)]:
            domains[(nr, nc)].remove(val)
            removed.append((nr, nc, val))
            if len(domains[(nr, nc)]) == 0:
                return False, removed
    return True, removed


def restore(domains, removed):
    for r, c, v in removed:
        domains[(r, c)].add(v)


def assign_single_domains(grid, domains):
    """
    Assign all cells that have exactly one remaining value.
    """
    changed = True
    while changed:
        changed = False
        for (r, c), dom in domains.items():
            if grid[r][c] == 0 and len(dom) == 1:
                val = next(iter(dom))
                grid[r][c] = val
                prune(domains, r, c, val)
                changed = True


def select_mrv(domains, grid):
    unassigned = [
        (cell, len(domains[cell]))
        for cell in domains
        if grid[cell[0]][cell[1]] == 0
    ]

    if not unassigned:
        return None

    return min(unassigned, key=lambda x: x[1])[0]


def solve(grid, domains):
    assign_single_domains(grid, domains)

    if is_complete(grid):
        return True

    cell = select_mrv(domains, grid)
    if cell is None:
        return False

    r, c = cell

    for val in sorted(domains[(r, c)]):
        grid[r][c] = val
        old_domain = domains[(r, c)]
        domains[(r, c)] = {val}

        ok, removed = forward_check(domains, r, c, val)
        if ok and solve(grid, domains):
            return True

        # Backtrack
        grid[r][c] = 0
        domains[(r, c)] = old_domain
        restore(domains, removed)

    return False

if __name__ == "__main__":

    sudoku = [
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

    print("Initial Sudoku:")
    print_grid(sudoku)

    domains = init_domains(sudoku)

    if solve(sudoku, domains):
        print("Solved Sudoku:")
        print_grid(sudoku)
    else:
        print("No solution found.")