import json
from concurrent import futures

import calendar_solver.generated.calendar_tetromino_pb2 as calendar_tetromino_pb2
import calendar_solver.generated.calendar_tetromino_pb2_grpc as calendar_tetromino_pb2_grpc
import grpc
from calendar_solver.calendar_solver.calendar_solver import \
    CalenderSolver  # your logic here
from calendar_solver.calendar_solver.util import (format_day_of_week,
                                                  format_month)


class tetrominoSolverServicer(calendar_tetromino_pb2_grpc.tetrominoSolverServicer):
    def SolvePuzzle(self, request, context):
        date = request.date.ToDatetime()  # Convert protobuf Timestamp to datetime.datetime

        solver = CalenderSolver(date.year, format_month(date.month), date.day, format_day_of_week(date.weekday()))
        solution, _ = solver.solve_exact_cover(first_solution_only=True)

        return self._build_placement(solution)

    def SolvePuzzleAllSolutions(self, request, context):
        date = request.date.ToDatetime()  # Convert protobuf Timestamp to datetime.datetime

        solver = CalenderSolver(date.year, format_month(date.month), date.day, format_day_of_week(date.weekday()))
        solution, all_solutions = solver.solve_exact_cover()

        # some solutions are exactly the same, so we need to remove duplicates
        solutions = []
        for solution in all_solutions:
            solutions.append(self._build_placement(solution))
        
        return calendar_tetromino_pb2.PuzzleSolutions(
            solutions=solutions
        )

    def _build_placement(self, solution):
        pieces = []
        transformed_solution = {}
        
        for step in solution:
            cells = []
            for item in step:
                if "piece" in item:
                    piece_name = item
                    transformed_solution[piece_name] = []
                else:
                    row, col = map(int, item.split("_")[1:])
                    cells.append(calendar_tetromino_pb2.Cell(row=str(row), col=str(col)))
                    
            piece = calendar_tetromino_pb2.Piece(
                tetromino_name=piece_name,
                cells=cells
            )
            pieces.append(piece)
            
        return calendar_tetromino_pb2.PuzzleSolution(solution_pieces=pieces)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calendar_tetromino_pb2_grpc.add_tetrominoSolverServicer_to_server(tetrominoSolverServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("🟢 gRPC server listening at [::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
if __name__ == "__main__":
    serve()
