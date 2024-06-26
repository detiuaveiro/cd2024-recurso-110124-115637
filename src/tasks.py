from _celery import app
from sudoku import Sudoku
import logging


logging.basicConfig(level=logging.INFO, filename="tasks.log")
logger = logging.getLogger(__name__)
logger.info("Tasks module loaded")

@app.task(name="tasks.generate_possible_puzzles")
def generate_possible_puzzles(task):
    """Generates all possible puzzles for a 3x3 subgrid"""
    subgrid = task["subgrid"]
    id = task["id"]
    logger.info(f"Gera sub-puzzles para {id} : {subgrid}")
    print(f"Gera sub-puzzles para {id} : {subgrid}")

    possible_puzzles = []
    
    sudoku = Sudoku()
    possible_puzzles = sudoku.generate_possibilities(subgrid)
    print("possible_puzzles", possible_puzzles)
    return possible_puzzles


@app.task(name="tasks.validate_line")
def validate_line(task):
    """Validates a 3x9 line of a sudoku puzzle"""
    line = task["lines"]
    id = task["id"]
    logger.info(f"Validando linha {id} : {line}")
    print(f"Validando linha {id} : {line}")

    sudoku = Sudoku(line)
    
    if sudoku.checkx9():
        return line
    else:
        return False
    

@app.task(name="tasks.check_puzzle")
def check_puzzle(task):
    """Checks a 9x9 sudoku puzzle"""
    puzzle = task["puzzle"]
    id = task["id"]
    logger.info(f"Validando puzzle {id} : {puzzle}")
    print(f"Validando puzzle {id} : {puzzle}")
    
    sudoku = Sudoku(puzzle)
    
    if sudoku.check():
        return puzzle
    else:
        return False
