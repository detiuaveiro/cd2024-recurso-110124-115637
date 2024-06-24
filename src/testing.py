# def divide_into_sub_puzzles(sudoku):
#     sub_puzzles = []

#     for row in range(0, 9, 3):
#         for col in range(0, 9, 3):
#             sub_puzzle = []
#             for r in range(row, row + 3):
#                 sub_puzzle_row = sudoku[r][col:col + 3]
#                 sub_puzzle.append(sub_puzzle_row)
#             sub_puzzles.append(sub_puzzle)

#     return sub_puzzles

# # Exemplo de uso:
# sudoku = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ]

# sub_puzzles = divide_into_sub_puzzles(sudoku)
# for i, sp in enumerate(sub_puzzles, 1):
#     print(f"Sub-puzzle {i}:")
#     for row in sp:
#         print(row)
#     print()


import itertools

def is_valid_sub_puzzle(sub_puzzle):
    # Check if the current sub-puzzle configuration is valid
    nums = [num for row in sub_puzzle for num in row if num != 0]
    return len(nums) == len(set(nums))

def generate_possibilities(sub_puzzle):
    # Find all empty positions
    empty_positions = [(i, j) for i in range(3) for j in range(3) if sub_puzzle[i][j] == 0]

    # Generate all combinations of numbers 1-9 for the empty positions
    all_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    existing_numbers = {num for row in sub_puzzle for num in row if num != 0}
    possible_numbers = [num for num in all_numbers if num not in existing_numbers]

    possibilities = []

    for combination in itertools.product(possible_numbers, repeat=len(empty_positions)):
        new_sub_puzzle = [row[:] for row in sub_puzzle]  # Copy the sub-puzzle

        for (i, j), num in zip(empty_positions, combination):
            new_sub_puzzle[i][j] = num

        if is_valid_sub_puzzle(new_sub_puzzle):
            possibilities.append(new_sub_puzzle)

    return possibilities

# Exemplo de uso:
sub_puzzle = [
    [9, 1, 4],
    [8, 2, 3],
    [5, 0, 0]
]

possibilities = generate_possibilities(sub_puzzle)
for i, possibility in enumerate(possibilities ,1):
    print(f"Possibility {i}:")
    for row in possibility:
        print(row)
    print()
