import json
from concurrent import futures

import grpc

import calendar_solver.generated.calendar_tetrino_pb2 as calendar_tetrino_pb2
import calendar_solver.generated.calendar_tetrino_pb2_grpc as calendar_tetrino_pb2_grpc
from calendar_solver.calendar_solver.calendar_solver import CalenderSolver  # your logic here
from calendar_solver.calendar_solver.util import format_day_of_week, format_month


class TetrinoSolverServicer(calendar_tetrino_pb2_grpc.TetrinoSolverServicer):
    def SolvePuzzle(self, request, context):
        date = request.date.ToDatetime()  # Convert protobuf Timestamp to datetime.datetime

        solver = CalenderSolver(date.year, format_month(date.month), date.day, format_day_of_week(date.weekday()))
        solution, _ = solver.solve_exact_cover()

        return self._build_placement(solution)

    def SolvePuzzleAllSolutions(self, request, context):
        date = request.date.ToDatetime()  # Convert protobuf Timestamp to datetime.datetime

        solver = CalenderSolver(date.year, format_month(date.month), date.day, format_day_of_week(date.weekday()))
        solution, all_solutions = solver.solve_exact_cover()

        # some solutions are exactly the same, so we need to remove duplicates
        solutions = []
        for solution in all_solutions:
            solutions.append(self._build_placement(solution))
        
        return calendar_tetrino_pb2.PuzzleSolutions(
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
                    cells.append(calendar_tetrino_pb2.Cell(row=str(row), col=str(col)))
                    
            piece = calendar_tetrino_pb2.Piece(
                tetrino_name=piece_name,
                cells=cells
            )
            pieces.append(piece)
            
        return calendar_tetrino_pb2.PuzzleSolution(solution_pieces=pieces)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calendar_tetrino_pb2_grpc.add_TetrinoSolverServicer_to_server(TetrinoSolverServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("🟢 gRPC server listening at [::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
