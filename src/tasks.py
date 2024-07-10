from _celery import app
from sudoku import Sudoku
import logging
import redis, json
import os
from dotenv import load_dotenv

# start redis
load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
if not REDIS_HOST:
    REDIS_HOST = 'localhost'


r = redis.Redis(host=REDIS_HOST, port=6379, db=1)

handicap = int(r.get("handicap") or 1)

logging.basicConfig(level=logging.INFO, filename="tasks.log")
logger = logging.getLogger(__name__)
logger.info("Tasks module loaded")

@app.task(name="tasks.generate_possible_puzzles", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def generate_possible_puzzles(task):
    
    """Generates all possible puzzles for a 3x3 subgrid"""
    subgrid = task["subgrid"]
    id = task["id"]

    # ver se já gerei esse subgrid antes
    key = json.dumps(subgrid)
    if r.exists(key):
        value = r.get(key)
        return json.loads(value)


    logger.info(f"Gera sub-puzzles para {id} : {subgrid}")
    print(f"Gera sub-puzzles para {id} : {subgrid}")

    possible_puzzles = []
    
    sudoku = Sudoku()
    possible_puzzles = sudoku.generate_possibilities(subgrid)
    print("possible_puzzles", possible_puzzles)

    # guardar na cachez
    value_to_cache = json.dumps(possible_puzzles)
    r.set(key, value_to_cache)
    
    return possible_puzzles


@app.task(name="tasks.validate_line", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def validate_line(task):
    """Validates a 3x9 line of a sudoku puzzle"""
    line = task["lines"]
    id = task["id"]
    logger.info(f"Validando linha {id} : {line}")
    print(f"Validando linha {id} : {line}")

    sudoku = Sudoku(line, base_delay=handicap)
    
    if sudoku.checkx9():
        return line
    else:
        return False
    

@app.task(name="tasks.check_puzzle", autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def check_puzzle(task):
    """Checks a 9x9 sudoku puzzle"""
    puzzle = task["puzzle"]
    id = task["id"]
    logger.info(f"Validando puzzle {id} : {puzzle}")
    print(f"Validando puzzle {id} : {puzzle}")
    
    sudoku = Sudoku(puzzle, base_delay=handicap)
    
    if sudoku.check():
        return puzzle
    else:
        return False
