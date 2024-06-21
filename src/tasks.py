from .celery import app
from sudoku import Sudoku

@app.task
def generate_possible_puzzles(subgrid):
    """Generates all possible puzzles for a 3x3 subgrid"""
    possible_puzzles = []
    
    sudoku = Sudoku([])
    possible_puzzles = sudoku.generate_possibilities(subgrid)
                    
    return possible_puzzles