from flask import Flask, request, jsonify
from tasks import generate_possible_puzzles
from sudoku import Sudoku
# from cache import cache_result, get_cached_result
import json, uuid
import argparse
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

pool = ThreadPoolExecutor(10)

def handle_puzzle(puzzle: list[list[int]], id:str):
    sudoku = Sudoku(puzzle)
    sub_puzzles =sudoku.generate_sub_puzzles()
    print("sub_puzzles", len(sub_puzzles))

    # Enviar para o broker
    task = [generate_possible_puzzles.delay(subgrid) for subgrid in sub_puzzles]
    print("task", task)

    # Esperar que todas as tarefas terminem e juntar os resultados
    results = [t.get() for t in task]
    print("results")
    for n, result in enumerate(results, 1):
        print(f'result {n}: {result}')

def generate_puzzle_id():
    # return str(hash(tuple(map(tuple, puzzle))))
    return str(uuid.uuid4())

@app.route('/solve', methods=['POST'])
def solve_puzzle():
    data = request.get_json()
    puzzle = data.get('sudoku')
    
    if puzzle:
        puzzle_id = generate_puzzle_id()
        pool.submit(handle_puzzle, puzzle, puzzle_id)
        # handle_puzzle(puzzle, puzzle_id)

        print("received a puzzle to solve", puzzle_id)
        return puzzle_id
    return jsonify({"error": "Invalid puzzle"}), 400

@app.route('/solution/<puzzle_id>', methods=['GET'])
def get_solution(puzzle_id):
    # result = get_cached_result(puzzle_id)
    result = f"solution{puzzle_id}"
    if result:
        return jsonify({"solution": result})
    return jsonify({"error": "Solution not found"}), 404


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sudoku Solver Master Server')
    parser.add_argument("-p", "--port", type=int, help='Port to run the server on', default=8001)
    parser.add_argument("-d", "--handicap", type=bool, help='Handicap', default=1)
    args = parser.parse_args()
    http_port = args.port
    handicap = args.handicap

    app.run(port=http_port)
