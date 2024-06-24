from _celery import app
from sudoku import Sudoku
import logging


logging.basicConfig(level=logging.INFO, filename="tasks.log")
logger = logging.getLogger(__name__)
logger.info("Tasks module loaded")

@app.task(name="tasks.generate_possible_puzzles")
def generate_possible_puzzles(task):
    """Generates all possible puzzles for a 3x3 subgrid"""
    subgrid = task
    possible_puzzles = []
    
    sudoku = Sudoku()
    possible_puzzles = sudoku.generate_possibilities(subgrid)
    print("possible_puzzles", possible_puzzles)
    return possible_puzzles