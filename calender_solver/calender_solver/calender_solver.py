import copy

import dlx
from tetrino import Shape, Tetrino
from util import DayOfWeek, Month, get_calender_order


class CalenderGrid():
    def __init__(self):
        self.rows = 8
        self.cols = 7
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self._init_calender_grid()

        self.grid_values = {}
        self._init_grid_values()

    def __repr__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    def _init_calender_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = 0

        self.grid[0][6] = None
        self.grid[1][6] = None
        self.grid[7][0] = None
        self.grid[7][1] = None
        self.grid[7][2] = None
        self.grid[7][3] = None

    def _init_grid_values(self):
        calender_order = get_calender_order()
        order_index = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 0:
                    self.grid_values[calender_order[order_index]] = (i, j)
                    order_index += 1

class CalenderSolver():
    def __init__(self, year: int, month: Month, day: int, day_of_week: DayOfWeek):
        self.year = year
        self.days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.days_in_month[1] += self.is_leap_year(year)

        self.tetrinos = {
            "small_L_tetrino": Tetrino(Shape(2, 3, [[1, 0], [1, 0], [1, 1]]), "sL"),
            "big_L_tetrino": Tetrino(Shape(2, 4, [[1, 0], [1, 0], [1, 0], [1, 1]]), "bL"),
            "long_L_tetrino": Tetrino(Shape(3, 3, [[1, 0, 0], [1, 0, 0], [1, 1, 1]]), "lL"),
            "lowercase_l_tetrino": Tetrino(Shape(1, 4, [[1], [1], [1], [1]]), "l"),
            "u_tetrino": Tetrino(Shape(3, 2, [[1, 0, 1], [1, 1, 1]]), "U"),
            "small_z_tetrino": Tetrino(Shape(3, 2, [[0, 1, 1], [1, 1, 0]]), "sZ"),
            "big_z_tetrino": Tetrino(Shape(4, 2, [[0, 0, 1, 1], [1, 1, 1, 0]]), "bZ"),
            "z_tetrino": Tetrino(Shape(3, 3, [[0, 1, 1], [0, 1, 0], [1, 1, 0]]), "Z"),
            "t_tetrino": Tetrino(Shape(3, 3, [[1, 1, 1], [0, 1, 0], [0, 1, 0]]), "T"),
            "p_tetrino": Tetrino(Shape(2, 3, [[1, 1], [1, 1], [1, 0]]), "P"),
        }

        self.calender_grid = CalenderGrid()
        self.empty_cells = []
        self._init_empty_cells(month, day, day_of_week)
        print(f"Empty cells: {self.empty_cells}")
        self._build_dlx_columns(self.calender_grid, self.empty_cells, self.tetrinos.keys())
        self._build_dlx_rows(self.tetrinos, self.calender_grid, self.empty_cells)
        self.build_dlx_matrix()

    def is_leap_year(self, year: int) -> int:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def _init_empty_cells(self, month, day, day_of_week):
        self.empty_cells = [
            self.calender_grid.grid_values[month.name],
            self.calender_grid.grid_values[day],
            self.calender_grid.grid_values[day_of_week.name]
        ]
        for cell in self.empty_cells:
            self.calender_grid.grid[cell[0]][cell[1]] = None
        return self.empty_cells
    
    def _build_dlx_columns(self, grid, empty_cells, tetrino_keys):
        self.columns = []

        # Add one column for every usable cell (non-None and not in empty_cells)
        for i in range(grid.rows):
            for j in range(grid.cols):
                if grid.grid[i][j] is not None and (i, j) not in empty_cells:
                    self.columns.append(("cell", (i, j)))

        # Add one column for each tetrino
        for name in tetrino_keys:
            self.columns.append(("piece", name))
            
    def count_shape_cells(self, shape_matrix):
        return sum(cell for row in shape_matrix for cell in row)
            
    def _build_dlx_rows(self, tetrinos, grid, empty_cells):
        self.rows = []
        
        for name, tetrino in tetrinos.items():
            base_shape = tetrino.shape
            for rotation in range(4):
                shape_variant = copy.deepcopy(base_shape)
                for _ in range(rotation):
                    shape_variant.rotate()

                expected_cells = self.count_shape_cells(shape_variant.shape)

                for row in range(grid.rows):
                    for col in range(grid.cols):
                        cells = []
                        valid = True

                        for i, shape_row in enumerate(shape_variant.shape):
                            for j, cell in enumerate(shape_row):
                                if cell:
                                    r = row + i
                                    c = col + j
                                    if (
                                        r >= grid.rows or c >= grid.cols or
                                        grid.grid[r][c] is None or
                                        (r, c) in empty_cells
                                    ):
                                        valid = False
                                        break
                                    cells.append(("cell", (r, c)))
                            if not valid:
                                break

                        if valid and len(cells) == expected_cells:
                            self.rows.append([("piece", name)] + cells)
        
        print(f"[DEBUG] Total DLX columns: {len(self.columns)}")
        print(f"[DEBUG] Generated {len(self.rows)} valid tetrino placements")
        
        from collections import defaultdict

        placement_counts = defaultdict(int)
        cell_coverage_counts = defaultdict(list)

        for row in self.rows:
            piece = [c for c in row if c[0] == 'piece'][0][1]
            cell_count = len([c for c in row if c[0] == 'cell'])
            placement_counts[piece] += 1
            cell_coverage_counts[piece].append(cell_count)

        print("=== Tetrino Placement Stats ===")
        for piece in sorted(placement_counts.keys()):
            placements = placement_counts[piece]
            unique_coverage = set(cell_coverage_counts[piece])
            print(f"{piece}: {placements} placements | Cell counts: {list(unique_coverage)}")
                            
    def build_dlx_matrix(self):
        # Map each column to an index
        column_index_map = {col: i for i, col in enumerate(self.columns)}
        
        print("Sample column:", self.columns[0])
        print("Sample row:", self.rows[0])
        
        all_column_labels = set(self.columns)
        for row in self.rows:
            for constraint in row:
                if constraint not in all_column_labels:
                    print("[ERROR] Row has constraint not in columns:", constraint)

        # Convert each constraint row to index-based row
        self.matrix_rows = []
        for row in self.rows:
            matrix_row = [column_index_map[constraint] for constraint in row]
            self.matrix_rows.append(matrix_row)

        return self.matrix_rows
    
    def solve_exact_cover(self):
        solver = dlx.DLX(self.columns)
        for row in self.matrix_rows:
            solver.appendRow(row)

        # If you want all the solutions
        # solutions = list(solver.solve())
        first_solution = next(solver.solve(), None)
        return first_solution

    def apply_solution_to_grid(self, solution_indices, rows, grid):
        for index in solution_indices:
            placement = rows[index]
            piece_label = None
            for constraint in placement:
                if constraint[0] == "piece":
                    piece_label = constraint[1]
                elif constraint[0] == "cell":
                    i, j = constraint[1], constraint[2]
                    grid.grid[i][j] = piece_label

if __name__ == "__main__":
    year = 2025
    month = Month.APR
    day = 24
    day_of_week = DayOfWeek.THU
    print(f"{day_of_week.name} {year}/{month.value}/{day}")

    solver = CalenderSolver(year, month, day, day_of_week)
    solution = solver.solve_exact_cover()
    print(solution)

    p = solver.tetrinos["p_tetrino"].shape.shape
    print(p)
        # Apply 3 clockwise rotations
    for _ in range(3):
        p = list(zip(*p[::-1]))  # 90° clockwise

    print("Rotation 3:")
    for row in p:
        print(row)

    if solution:
        solver.apply_solution_to_grid(solution[0])
        print("Solved Grid:")
        print(solver.grid)
    else:
        print("No solution found.")
