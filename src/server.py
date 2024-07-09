from flask import Flask, request, jsonify
from tasks import generate_possible_puzzles, validate_line, check_puzzle
from sudoku import Sudoku
# from cache import cache_result, get_cached_result
import json, uuid
import argparse
from concurrent.futures import ThreadPoolExecutor

import os
from dotenv import load_dotenv
import redis
import time

app = Flask(__name__)
# start redis
load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
if not REDIS_HOST:
    REDIS_HOST = 'localhost'

r = redis.Redis(host=REDIS_HOST, port=6379, db=1)

# push context manually to app
with app.app_context():
    # clean up the cache
    r.flushdb()

    # set solved default to 0
    r.set("solved", 0)

pool = ThreadPoolExecutor(10)

def puzzle_to_string(puzzle):
    """Convert a puzzle to a string"""
    return json.dumps(puzzle)

def get_cached_result(puzzle):
    """Get the cached result for a puzzle"""
    result = r.get(puzzle_to_string(puzzle))

    if result:
        return json.loads(result)
    return None

def validate_quadrant(line_results, id, quadrant_number):
    """Validate a 3x9 quadrant of a sudoku puzzle"""
    print(f"Validating quadrant {quadrant_number} for {id}")
    tasks = [validate_line.delay({"lines": lines, "id": id}) for lines in line_results]
    results = [t.get() for t in tasks]
    
    valid_results = [result for result in results if result]
    
    return valid_results

def handle_puzzle(puzzle: list[list[int]], id:str):
    start_time = time.time()
    print(f"Received puzzle {puzzle}, id {id}")

    # check if puzzle is in cache
    result = get_cached_result(puzzle)
    if result:
        # save_result(id, result)
        r.set(id, json.dumps(result))

        # increment solved
        r.incr("solved")
        
        print("Returned cached result")
        return

    sudoku = Sudoku(puzzle)

    print("Solving puzzle", id)

    # Gerar sub-puzzles
    sub_puzzles =sudoku.generate_sub_puzzles()
    # print("sub_puzzles", len(sub_puzzles))

    # Enviar para o broker
    task = [generate_possible_puzzles.delay({
        "subgrid": subgrid, "id": id})
        for subgrid in sub_puzzles]
    
    # print("task", task)

    # Esperar que todas as tarefas terminem e juntar os resultados
    results = [t.get() for t in task]
    # print("results")
    # for n, result in enumerate(results, 1):
    #     print(f'result {n}: {result}')

    # combinar e gerar linhas

    line1 =  results[0], results[1], results[2]
    line2 =  results[3], results[4], results[5]
    line3 =  results[6], results[7], results[8]

    line1_results = sudoku.combine_sub_in_lines(line1[0], line1[1], line1[2])
    # print("line1_results", len(line1_results), line1_results)
    line2_results = sudoku.combine_sub_in_lines(line2[0], line2[1], line2[2])
    # print("line2_results", len(line2_results), line2_results)
    line3_results = sudoku.combine_sub_in_lines(line3[0], line3[1], line3[2])
    # print("line3_results", len(line3_results), line3_results)

    
    # Validar os três quadrantes
    # #  send first 3x9 for validations
    quadrant1 = validate_quadrant(line1_results, id, 1)

    # # send second 3x9 for validations
    quadrant2 = validate_quadrant(line2_results, id, 2)

    # # send third 3x9 for validations
    quadrant3 = validate_quadrant(line3_results, id, 3)


    # combinar e gerar puzzles
    puzzles = sudoku.generate_puzzles(quadrant1, quadrant2, quadrant3)
    print("Generated ",len(puzzles), "puzzles for ", id)
    task = [check_puzzle.delay(
        {"puzzle": puzzle, "id": id})
        for puzzle in puzzles]

    results = [t.get() for t in task if t.get()]
    result = results[0]
    print(f"Solved puzzle {id} in {time.time() - start_time} seconds")
    sudoku = Sudoku(result)
    print(sudoku)

    # save_result(id, result)
    r.set(id, json.dumps(result))

    # increment solved
    r.incr("solved")

    # cache_result(id, result)
    r.set(puzzle_to_string(puzzle), puzzle_to_string(result))



def generate_puzzle_id():
    """Generate a unique id for the puzzle"""
    # return str(hash(tuple(map(tuple, puzzle))))
    return str(uuid.uuid4())

@app.route('/solve', methods=['POST'])
def solve_puzzle():
    """Solve a sudoku puzzle"""
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
    """Get the solution to a puzzle"""
    # result = get_cached_result(puzzle_id)
    result = r.get(puzzle_id)
    if result:
        return jsonify(json.loads(result))
    print('result: ', result)
    solved = r.get("solved")
    return solved 


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sudoku Solver Master Server')
    parser.add_argument("-p", "--port", type=int, help='Port to run the server on', default=8001)
    parser.add_argument("-d", "--handicap", type=int, help='Handicap', default=1)
    args = parser.parse_args()
    http_port = args.port
    handicap = args.handicap
    
    r.set("handicap", handicap)

    app.run(port=http_port)
