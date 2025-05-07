import copy

import dlx
from tetrino import Shape, Tetrino
from util import DayOfWeek, Month, get_calender_order, get_today


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
        """ Initialize the grid with unusable cells that are defined by the
            puzzle grid's irregular shape.
        """
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
        """ Initialize the grid values with the calendar order.
            The grid values are the labels of the cells in the grid.
        """
        calender_order = get_calender_order()
        order_index = 0

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 0:
                    self.grid_values[calender_order[order_index]] = (i, j)
                    order_index += 1

class CalenderSolver():
    """ Class to solve the calendar puzzle using DLX algorithm."""
    def __init__(self, year: int, month: Month, day: int, day_of_week: DayOfWeek):
        self.year = year
        self.days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.is_leap_year(year):
            self.days_in_month[1] += 1

        self.calender_grid = CalenderGrid()
        self._init_empty_cells(month, day, day_of_week)
        self._init_tetrinos()

        self._build_dlx_columns(self.calender_grid, self.empty_cells, self.tetrinos.keys())
        self._build_dlx_rows(self.tetrinos, self.calender_grid, self.empty_cells)

    def is_leap_year(self, year: int) -> bool:
        """Check if a year is a leap year.
        
        :param year: The year to check.
        :return: True if the year is a leap year
        """
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def _init_tetrinos(self):
        """ Initialize the tetrinos with their shapes and names.
            INTERNAL USE ONLY.
        """
        self.tetrinos = {
            "small_L_tetrino": Tetrino(Shape(2, 3, [[1, 0], [1, 0], [1, 1]]), "sL"),
            "big_L_tetrino": Tetrino(Shape(2, 4, [[1, 0], [1, 0], [1, 0], [1, 1]]), "bL"),
            "symmetrical_L_tetrino": Tetrino(Shape(3, 3, [[1, 0, 0], [1, 0, 0], [1, 1, 1]]), "symL"),
            "lowercase_l_tetrino": Tetrino(Shape(1, 4, [[1], [1], [1], [1]]), "l"),
            "u_tetrino": Tetrino(Shape(3, 2, [[1, 0, 1], [1, 1, 1]]), "U"),
            "small_z_tetrino": Tetrino(Shape(3, 2, [[1, 1, 0], [0, 1, 1]]), "sZ"),
            "big_z_tetrino": Tetrino(Shape(4, 2, [[0, 0, 1, 1], [1, 1, 1, 0]]), "bZ"),
            "z_tetrino": Tetrino(Shape(3, 3, [[0, 1, 1], [0, 1, 0], [1, 1, 0]]), "Z"),
            "t_tetrino": Tetrino(Shape(3, 3, [[1, 1, 1], [0, 1, 0], [0, 1, 0]]), "T"),
            "p_tetrino": Tetrino(Shape(2, 3, [[1, 1], [1, 1], [1, 0]]), "P"),
        }

    
    def _init_empty_cells(self, month, day, day_of_week):
        """ Initialize the empty cells in the grid with the month, day, and 
            day of week.
            INTERNAL USE ONLY.
            
            :param month: The month to set.
            :param day: The day to set.
            :param day_of_week: The day of the week to set.
        """
        self.empty_cells = [
            self.calender_grid.grid_values[month.name],
            self.calender_grid.grid_values[day],
            self.calender_grid.grid_values[day_of_week.name]
        ]
    
    def _build_dlx_columns(self, grid, empty_cells, tetrino_keys):
        """ Build the columns for the DLX algorithm.
            INTERNAL USE ONLY.
            
            :param grid: The grid to use.
            :param empty_cells: The empty cells in the grid.
            :param tetrino_keys: The keys of the tetrinos to use.
        """
        self.columns = []

        # Add one column for every usable cell (non-None and not in empty_cells)
        for i in range(grid.rows):
            for j in range(grid.cols):
                if grid.grid[i][j] is not None and (i, j) not in empty_cells:
                    self.columns.append((f"cell_{i}_{j}", dlx.DLX.PRIMARY))
                if (i, j) in empty_cells:
                    self.columns.append((f"cell_{i}_{j}", dlx.DLX.SECONDARY))
                    
        # Add one column for each tetrino
        for name in tetrino_keys:
            self.columns.append((f"piece_{name}", dlx.DLX.PRIMARY))
            
        # index the cells and the pieces to an indexable metadata format
        self.col_index = {col[0]: idx for idx, col in enumerate(self.columns)}
            
    def _build_dlx_rows(self, tetrinos, grid, empty_cells):
        """ Build the rows for the DLX algorithm.
            INTERNAL USE ONLY.
            
            :param tetrinos: The tetrinos to use.
            :param grid: The grid to use.
            :param empty_cells: The empty cells in the grid.
        """
        self.rows = []
        self.row_metadata = []
        
        for name, tetrino in tetrinos.items():
            for rotation in range(4):
                rotated_tetrino = copy.deepcopy(tetrino)
                rotated_tetrino.rotate_clockwise(90 * rotation)

                shape_matrix = rotated_tetrino.shape.shape
                expected_cells = sum(cell for row in shape_matrix for cell in row)
                    
                print(f"[DEBUG] {name} rotation {rotation}: {shape_matrix}")

                for row in range(grid.rows):
                    for col in range(grid.cols):
                        cells = []
                        valid = True

                        for i, shape_row in enumerate(shape_matrix):
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
                                    cells.append((r, c))
                            if not valid:
                                break

                        if valid and len(cells) == expected_cells:                            
                            # A possible iteration of the tetrino in an
                            # indexed Intermediate Representation form 
                            dlx_row = [self.col_index[f"piece_{name}"]] + \
                                [self.col_index[f"cell_{r}_{c}"] for (r,c) in \
                                    cells]
                            self.rows.append(dlx_row)
                            self.row_metadata.append((name, rotation, cells))
    
    def solve_exact_cover(self):
        """ Solve the exact cover problem using the DLX algorithm.
            :return: The solution to the exact cover problem.
        """
        # print("[DEBUG] DLX columns:", self.columns)
        # # print("[DEBUG] DLX column index:", self.col_index)
        # print("[DEBUG] DLX rows:", self.rows)
        
        # print("[DEBUG] Number of rows:", len(self.rows))
        # print("[DEBUG] Number of columns:", len(self.columns))
        solver = dlx.DLX(self.columns)
        for i, row in enumerate(self.rows):
            solver.appendRow(row, i)  # <-- append with label `i`
        
        solutions = solver.solve()
        
        # get all unique solutions
        solutions = set(tuple(sorted(solution)) for solution in solutions)
        
        solution = list(solutions)[0]
        print("[DEBUG] Solution rows:", solution)
        if solution is None:
            return [], []
        else:
            solution_rows = []
            for i in solution:
                solution_rows.append(solver.getRowList(i))
            return solution_rows, solutions

    def apply_solution_to_grid(self, solution_rows):
        """
        Applies the solution rows directly onto the calendar grid.

        :param solution_rows: List of lists, where each sublist contains cell names and one piece name.
        :return: The final solved grid.
        """
        for row in solution_rows:
            piece = None
            cells = []
            
            for col in row:
                if col.startswith("piece_"):
                    piece = col.replace("piece_", "")  # e.g., 'piece_tetrino' -> 'tetrino'
                    piece = self.tetrinos[piece].name
                elif col.startswith("cell_"):
                    _, r, c = col.split("_")
                    r = int(r)
                    c = int(c)
                    cells.append((r, c))

            if piece is None:
                raise ValueError("Piece name missing in row!")

            for r, c in cells:
                self.calender_grid.grid[r][c] = piece

        return self.calender_grid.grid


if __name__ == "__main__":
    days_forward = int(input("How many days forward? (i.e. 0=today, 1=tomorow, 2=...): "))
    year, month, day, day_of_week = get_today(days_forward)
    print("[DEBUG] Today's date:", year, month, day, day_of_week)

    solver = CalenderSolver(year, month, day, day_of_week)
    solution, all_possible_solutions = solver.solve_exact_cover()
    print("[DEBUG] Solution:", solution)
    if solution:
        grid = solver.apply_solution_to_grid(solution)
        for row in grid:
            print(" ".join(str(cell).ljust(4) for cell in row))
    else:
        print("No solution found.")
        