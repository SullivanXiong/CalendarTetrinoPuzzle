from datetime import datetime, timezone

import calendar_solver.generated.calendar_tetromino_pb2 as calendar_tetromino_pb2
import calendar_solver.generated.calendar_tetromino_pb2_grpc as calendar_tetromino_pb2_grpc
import grpc
from google.protobuf.timestamp_pb2 import Timestamp


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = calendar_tetromino_pb2_grpc.TetrominoSolverStub(channel)

    # Create a Timestamp for today's date
    now = datetime.now(timezone.utc)
    timestamp = Timestamp()
    timestamp.FromDatetime(now)

    # Prepare request
    request = calendar_tetromino_pb2.PuzzleRequest(date=timestamp)

    # Call SolvePuzzle
    response = stub.SolvePuzzle(request)
    print("🧩 SolvePuzzle (single solution):")
    for piece in response.solution_pieces:
        print_piece(piece)

    # Call SolvePuzzleAllSolutions
    all_response = stub.SolvePuzzleAllSolutions(request)
    print("\n🧩 SolvePuzzleAllSolutions (multiple solutions):")
    for i, solution in enumerate(all_response.solutions):
        print(f"\nSolution #{i + 1}")
        for piece in solution.solution_pieces:
            print_piece(piece)

def print_piece(piece):
    cell_list = [(cell.row, cell.col) for cell in piece.cells]
    print(f"{piece.tetromino_name}:  @ {cell_list}")

if __name__ == "__main__":
    run()
