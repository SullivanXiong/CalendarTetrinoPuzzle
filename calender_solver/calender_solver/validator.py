from collections import defaultdict
from copy import deepcopy

import dlx
import pandas as pd
from tetrino import Shape, Tetrino
from util import get_calender_order

# Define the grid size and cutouts
rows, cols = 8, 7
cutouts = {(0, 6), (1, 6), (7, 0), (7, 1), (7, 2), (7, 3)}

# Load calendar order to get accurate reserved cells
calender_order = get_calender_order()
calender_grid_values = {}
index = 0
for i in range(rows):
    for j in range(cols):
        if (i, j) not in cutouts:
            calender_grid_values[calender_order[index]] = (i, j)
            index += 1

# Define reserved cells using accurate calendar labels
reserved = {
    calender_grid_values["APR"],  # month
    calender_grid_values[25],     # day
    calender_grid_values["FRI"]   # weekday
}

print("Reserved cells:", reserved)

unusable = cutouts | reserved

# Define tetrino shapes (updated to match physical puzzle)
shapes = {
    "T": Shape(3, 3, [[1, 1, 1], [0, 1, 0], [0, 1, 0]]),
    "sL": Shape(2, 3, [[1, 0], [1, 0], [1, 1]]),
    "lL": Shape(3, 3, [[1, 0, 0], [1, 0, 0], [1, 1, 1]]),
    "P": Shape(2, 3, [[0, 1], [1, 1], [1, 1]]),
    "sZ": Shape(3, 2, [[1, 1, 0], [0, 1, 1]]),
    "Z": Shape(3, 3, [[0, 1, 1], [0, 1, 0], [1, 1, 0]]),
    "bZ": Shape(2, 4, [[1, 0], [1, 0], [1, 1], [0, 1]]),
    "U": Shape(2, 3, [[1, 1], [1, 0], [1, 1]]),
    "bL": Shape(2, 4, [[1, 1], [0, 1], [0, 1], [0, 1]]),
    "l": Shape(4, 1, [[1, 1, 1, 1]])
}

rot = {
    "T": 1,
    "sL": 0,
    "lL": 0,
    "P": 1,
    "sZ": 0,
    "Z": 1,
    "bZ": 0,
    "U": 0,
    "bL": 0,
    "l": 1
}

tetrinos = {name: Tetrino(shape, name) for name, shape in shapes.items()}

# Manual layout from physical solution
manual_layout = {
    "T": [(2, 2), (3, 0), (3, 1), (3, 2), (4, 2)],
    "sZ": [(5, 1), (5, 2), (6, 2), (6, 3)],
    "sL": [(0, 0), (1, 0), (2, 0), (2, 1)],
    "lL": [(1, 5), (2, 5), (3, 3), (3, 4), (3, 5)],
    "P": [(0, 1), (0, 2), (1, 1), (1, 2), (1, 3)],
    "Z": [(0, 4), (0, 5), (1, 4), (2, 3), (2, 4)],
    "bZ": [(4, 5), (5, 5), (6, 5), (6, 6), (7, 6)],
    "U": [(4, 0), (4, 1), (5, 0), (6, 0), (6, 1)],
    "bL": [(4, 3), (4, 4), (5, 4), (6, 4), (7, 4)],
    "l": [(2, 6), (3, 6), (4, 6), (5, 6)],
}

# Convert manual layout into DLX rows and solve
columns = [("cell", (r, c)) for r in range(rows) for c in range(cols) if (r, c) not in unusable] + [("piece", name) for name in tetrinos]
col_index = {col: i for i, col in enumerate(columns)}

print("[DEBUG] Column index mapping:", col_index)

# take each value from the manual_layout and merge their lists
# into a single set of coordinates
manual_layout_coords = set()
for coords in manual_layout.values():
    manual_layout_coords.update(coords)
# Remove duplicates
generated_columns = {(r, c) for r in range(rows) for c in range(cols) if (r, c) not in unusable}

print("[DEBUG] manual_layout coords matches generated columns:", manual_layout_coords == generated_columns)

dlx_rows = []
row_metadata = []

for name, coords in manual_layout.items():
    row = [col_index[("piece", name)]] + [col_index[("cell", coord)] for coord in coords]
    dlx_rows.append(row)
    print(f"[DEBUG] Row for {name}: {row} {(name, rot[name], coords)}")
    row_metadata.append((name, rot[name], coords))  # assume rot 0 for now

# debug to check if all cells are covered by the dlx_rows
covered_cells = []
for row in dlx_rows:
    for col in row[1:]:
        covered_cells.append(col)
covered_cells.sort()
print("[DEBUG] Covered cells:", covered_cells)
print("[DEBUG] Generated cells:", columns)

dlx_columns = []
# convert from form ('cell', (r, c)) to [col_index] such as [('cell', (0, 0))]
# to [0] and [('piece', 'l')] to [56]
for col in columns:
    if col[0] == "cell":
        dlx_columns.append((f"cell{col_index[col]}", dlx.DLX.PRIMARY))
    else:
        dlx_columns.append((f"piece{col_index[col]-46}", dlx.DLX.PRIMARY))
        
print("[DEBUG] DLX columns:", dlx_columns)

# Diagnostic check for column coverage before solving
used_columns = defaultdict(int)
for row in dlx_rows:
    for col in row:
        used_columns[col] += 1

print("[DEBUG] Column coverage summary:")
missing_cols = []
duplicated_cols = []
for col, idx in col_index.items():
    count = used_columns[idx]
    if count == 0:
        print(f"[MISSING] {col}")
        missing_cols.append(col)
    elif count > 1 and col[0] == "piece":
        print(f"[DUPLICATE] {col} used {count} times")
        duplicated_cols.append(col)

if not missing_cols and not duplicated_cols:
    print("[PASS] All columns covered exactly once as required by exact cover.")
else:
    print("[WARN] Column mismatch may prevent DLX from solving.")

print("[DEBUG] DLX columns:", dlx_columns)
print("[DEBUG] DLX rows:", dlx_rows)

dlx_rows_cover_columns = set()
for row in dlx_rows:
    for col in row:
        dlx_rows_cover_columns.add(col)

print("[DEBUG] DLX rows covers all columns:", len(dlx_rows_cover_columns) == len(dlx_columns))

solver = dlx.DLX(dlx_columns)
rowNames = ['row%i' % i for i in range(len(dlx_rows))]
solver.appendRows(dlx_rows, rowNames)

solutions = list(solver.solve())
solution_rows = solutions[0] if solutions else []

solution_grid = [["." for _ in range(cols)] for _ in range(rows)]
decoded_solution = []

solver.printSolution(solutions[0])

print("[DEBUG] Solution rows:", solution_rows)
print("[DEBUG] Row metadata:", row_metadata)

for r in solution_rows:
    piece, rotation, cells = row_metadata[r]
    for (i, j) in cells:
        solution_grid[i][j] = piece
    decoded_solution.append((piece, rotation, cells))

if not decoded_solution:
    print("[FAIL] Manual layout not recoverable by DLX — mismatch detected.")
else:
    print("[INFO] Solution from manual layout test:")
    for piece, rot, cells in decoded_solution:
        print(f"{piece} (rot {rot}): {cells}")
