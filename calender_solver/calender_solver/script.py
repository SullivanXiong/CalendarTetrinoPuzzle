from collections import defaultdict
from copy import deepcopy

import dlx

# Define the grid size and cutouts
rows, cols = 8, 7
cutouts = {(0, 6), (1, 6), (7, 0), (7, 1), (7, 2), (7, 3)}
reserved = {(0, 3), (5, 2), (7, 4)}  # Reserved for date info
unusable = cutouts | reserved

# Define tetrino shapes
tetrinos = {
    "sL": [[1, 0], [1, 0], [1, 1]],
    "bL": [[1, 0], [1, 0], [1, 0], [1, 1]],
    "lL": [[1, 0, 0], [1, 0, 0], [1, 1, 1]],
    "l": [[1], [1], [1], [1]],
    "U": [[1, 0, 1], [1, 1, 1]],
    "sZ": [[0, 1, 1], [1, 1, 0]],
    "bZ": [[0, 0, 1, 1], [1, 1, 1, 0]],
    "Z": [[0, 1, 1], [0, 1, 0], [1, 1, 0]],
    "T": [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
    "P": [[1, 1], [1, 1], [1, 0]],
}

# Helper functions
def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def count_ones(shape):
    return sum(cell for row in shape for cell in row)

# Build DLX columns
cell_columns = [("cell", (r, c)) for r in range(rows) for c in range(cols) if (r, c) not in unusable]
piece_columns = [("piece", name) for name in tetrinos]
columns = cell_columns + piece_columns
col_index = {col: i for i, col in enumerate(columns)}

# Generate DLX rows
dlx_rows = []
placement_debug = defaultdict(int)
row_metadata = []

for name, base_shape in tetrinos.items():
    for rot in range(4):
        shape = deepcopy(base_shape)
        for _ in range(rot):
            shape = rotate(shape)
        h, w = len(shape), len(shape[0])
        expected_cells = count_ones(shape)

        for r in range(rows - h + 1):
            for c in range(cols - w + 1):
                cells = []
                valid = True
                for i in range(h):
                    for j in range(w):
                        if shape[i][j]:
                            pos = (r + i, c + j)
                            if pos in unusable:
                                valid = False
                                break
                            cells.append(("cell", pos))
                    if not valid:
                        break
                if valid and len(cells) == expected_cells:
                    row = [col_index[("piece", name)]] + [col_index[cell] for cell in cells]
                    dlx_rows.append(row)
                    row_metadata.append((name, rot, cells))
                    placement_debug[f"{name}_r{rot}"] += 1

# Solve DLX
solver = dlx.DLX(columns)
solver.appendRows(dlx_rows)

solutions = list(solver.solve())
print(solutions)
solution_rows = solutions[0] if solutions else []

solution_grid = [["." for _ in range(cols)] for _ in range(rows)]
decoded_solution = []

for r in solution_rows:
    piece, rotation, cells = row_metadata[r]
    for (i, j) in cells:
        solution_grid[i][j] = piece
    decoded_solution.append((piece, rotation, cells))

solution_grid, decoded_solution, placement_debug, len(solution_rows) if solutions else 0

# print(row_metadata)
# print(columns)
# print(dlx_rows)
print(solutions)

print("Solution Grid:")
for row in solution_grid:
    print(" ".join(row))