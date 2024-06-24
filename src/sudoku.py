import time
from collections import deque
import itertools



class Sudoku:
    def __init__(self, sudoku=[], base_delay=0.01, interval=10, threshold=5):
        self.grid = sudoku
        self.recent_requests = deque()
        self.check_count = 0
        self.base_delay = base_delay
        self.interval = interval
        self.threshold = threshold

    def _limit_calls(self, base_delay=0.01, interval=10, threshold=5):
        """Limit the number of requests made to the Sudoku object."""
        if base_delay is None:
            base_delay = self.base_delay
        if interval is None:
            interval = self.interval
        if threshold is None:
            threshold = self.threshold

        current_time = time.time()
        self.recent_requests.append(current_time)
        num_requests = len(
            [t for t in self.recent_requests if current_time - t < interval]
        )

        if num_requests > threshold:
            delay = base_delay * (num_requests - threshold + 1) # TODO: * o handicap ?
            time.sleep(delay)

        self.check_count += 1

    def __str__(self):
        string_representation = "| - - - - - - - - - - - |\n"

        for i in range(9):
            string_representation += "| "
            for j in range(9):
                string_representation += (
                    str(self.grid[i][j])
                    if self.grid[i][j] != 0
                    else f"\033[93m{self.grid[i][j]}\033[0m"
                )
                string_representation += " | " if j % 3 == 2 else " "

            if i % 3 == 2:
                string_representation += "\n| - - - - - - - - - - - |"
            string_representation += "\n"

        return string_representation

    def update_row(self, row, values):
        """Update the values of the given row."""
        self.grid[row] = values

    def update_column(self, col, values):
        """Update the values of the given column."""
        for row in range(9):
            self.grid[row][col] = values[row]

    def check_is_valid(
        self, row, col, num, base_delay=None, interval=None, threshold=None
    ):
        """Check if 'num' is not in the current row, column and 3x3 sub-box."""
        self._limit_calls(base_delay, interval, threshold)

        # Check if the number is in the given row or column
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        # Check if the number is in the 3x3 sub-box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False

        return True

    def check_row(self, row, base_delay=None, interval=None, threshold=None):
        """Check if the given row is correct."""
        self._limit_calls(base_delay, interval, threshold)

        # Check row
        if sum(self.grid[row]) != 45 or len(set(self.grid[row])) != 9:
            return False

        return True

    def check_column(self, col, base_delay=None, interval=None, threshold=None):
        """Check if the given row is correct."""
        self._limit_calls(base_delay, interval, threshold)

        # Check col
        if (
            sum([self.grid[row][col] for row in range(9)]) != 45
            or len(set([self.grid[row][col] for row in range(9)])) != 9
        ):
            return False

        return True

    def check_square(self, row, col, base_delay=None, interval=None, threshold=None):
        """Check if the given 3x3 square is correct."""
        self._limit_calls(base_delay, interval, threshold)

        # Check square
        if (
            sum([self.grid[row + i][col + j] for i in range(3) for j in range(3)]) != 45
            or len(
                set([self.grid[row + i][col + j] for i in range(3) for j in range(3)])
            )
            != 9
        ):
            return False

        return True

    def check(self, base_delay=None, interval=None, threshold=None):
        """Check if the given Sudoku solution is correct.

        You MUST incorporate this method without modifications into your final solution.
        """
        for row in range(9):
            if not self.check_row(row, base_delay, interval, threshold):
                return False

        # Check columns
        for col in range(9):
            if not self.check_column(col, base_delay, interval, threshold):
                return False

        # Check 3x3 squares
        for i in range(3):
            for j in range(3):
                if not self.check_square(i * 3, j * 3, base_delay, interval, threshold):
                    return False

        return True
    

    # my function to get sudoku line
    def get_line(self, row):
        return self.grid[row]
    

    def get_cell(self, row: int, col: int):
        return self.grid[row][col]
    

    def get_sudoku(self) -> list[list[int]]:
        """Returns the Sudoku grid."""
        return self.grid
    

    def get_check_count(self) -> int:
        """Returns the number of times the check() method was called."""
        return self.check_count
    

    def update_cell(self, row, col, value):
        self.grid[row][col] = value
    

    def update_sudoku(self, new_sudoku):
        self.grid = new_sudoku

    # my functions 

    def is_valid(self, puzzle, guess, row, col) -> bool:
   
        row_vals = puzzle[row]
        if guess in row_vals:
            return False
        

        col_vals = [puzzle[i][col] for i in range(9)]
        if guess in col_vals:
            return False
        

        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if puzzle[r][c] == guess:
                    return False
                
        return True  
    
    

    def generate_sub_puzzles(self):
        """Divide the Sudoku puzzle into 3x3 sub-puzzles."""
        sub_puzzles = []

        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                sub_puzzle = []
                for r in range(row, row + 3):
                    sub_puzzle_row = self.grid[r][col:col + 3]
                    sub_puzzle.append(sub_puzzle_row)
                sub_puzzles.append(sub_puzzle)

        return sub_puzzles
    


    def is_valid_sub_puzzle(self, sub_puzzle):
        """Check if the current sub-puzzle configuration is valid."""
        # Check if the current sub-puzzle configuration is valid
        nums = [num for row in sub_puzzle for num in row if num != 0]
        return len(nums) == len(set(nums))

    def generate_possibilities(self, sub_puzzle):
        """Generate all possible configurations for a 3x3 sub-puzzle."""
        # Find all empty positions
        empty_positions = [(i, j) for i in range(3) for j in range(3) if sub_puzzle[i][j] == 0]

        # Generate all combinations of numbers 1-9 for the empty positions
        all_numbers = [num for num in range(1, 10)]
        existing_numbers = {num for row in sub_puzzle for num in row if num != 0}
        possible_numbers = [num for num in all_numbers if num not in existing_numbers]

        possibilities = []

        for combination in itertools.product(possible_numbers, repeat=len(empty_positions)):
            new_sub_puzzle = [row[:] for row in sub_puzzle]  # Copy the sub-puzzle

            for (i, j), num in zip(empty_positions, combination):
                new_sub_puzzle[i][j] = num

            if self.is_valid_sub_puzzle(new_sub_puzzle):
                possibilities.append(new_sub_puzzle)

        return possibilities


    def solve_sudoku(self):
        if self.check():
            return True
        
        row, col = self.find_next_empty()


        for guess in range(1, 10):  # posteriormente, mudar para possible_numbers    
  
            if row is not None and col is not None:
                if self.check_is_valid(row, col, guess):
                    self.grid[row][col] = guess 

                    if self.solve_sudoku():
                        return True

                self.grid[row][col] = 0
        
        return False
    
    def combine_sub_puzzles(self, sub_puzzles):
        """Combine the 3x3 sub-puzzles into a 9x9 Sudoku puzzle."""
        sudoku = [[0 for _ in range(9)] for _ in range(9)]

        for i, sub_puzzle in enumerate(sub_puzzles):
            row = (i // 3) * 3
            col = (i % 3) * 3

            for r in range(3):
                for c in range(3):
                    sudoku[row + r][col + c] = sub_puzzle[r][c]

        return sudoku


if __name__ == "__main__":
    sudoku = Sudoku(
 [  [4, 2, 6, 5, 7, 1, 8, 9, 0], 
    [1, 9, 8, 4, 0, 3, 7, 5, 6], 
    [3, 5, 7, 8, 9, 6, 2, 1, 0], 
    [9, 6, 2, 3, 4, 8, 1, 7, 5], 
    [7, 0, 5, 6, 1, 9, 3, 2, 8], 
    [8, 1, 3, 7, 5, 0, 6, 4, 9],
    [5, 8, 1, 2, 3, 4, 9, 6, 7], 
    [6, 7, 9, 1, 8, 5, 4, 0, 2], 
    [2, 3, 4, 9, 6, 7, 5, 8, 1]]
    )

    print(sudoku)

    if sudoku.check():
        print("Sudoku is correct!")
    else:
        print("Sudoku is incorrect! Please check your solution.")


