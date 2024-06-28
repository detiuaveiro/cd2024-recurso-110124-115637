from _celery import app
from sudoku import Sudoku
import logging
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

handicap = int(r.get("handicap") or 1)

logging.basicConfig(level=logging.INFO, filename="tasks.log")
logger = logging.getLogger(__name__)
logger.info("Tasks module loaded")

@app.task(name="tasks.generate_possible_puzzles", bind=True)
def generate_possible_puzzles(self, task):
    try:
        """Generates all possible puzzles for a 3x3 subgrid"""
        subgrid = task["subgrid"]
        id = task["id"]
        logger.info(f"Gera sub-puzzles para {id} : {subgrid}")
        print(f"Print Gera sub-puzzles para {id} : {subgrid}")

        possible_puzzles = []
        
        sudoku = Sudoku()
        possible_puzzles = sudoku.generate_possibilities(subgrid)
        print("possible_puzzles", possible_puzzles)
        return possible_puzzles
    except Exception as e:
        self.retry(exc=e, countdown=5, max_retries=3)  


@app.task(name="tasks.validate_line", bind=True)
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
    

@app.task(name="tasks.check_puzzle", bind=True)
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
