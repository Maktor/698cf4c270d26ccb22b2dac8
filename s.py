import matplotlib.pyplot as plt
import random

def create_base_grid():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board

def solve_check(board):
    """
    Backtracking solver that returns the number of solutions found.
    Stops searching if more than 1 solution is found (puzzle is ambiguous).
    """
    find = find_empty(board)
    if not find:
        return 1
    row, col = find

    count = 0
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            count += solve_check(board)
            board[row][col] = 0  # Backtrack
            if count > 1: 
                return 2  # Found more than one solution, stop early
    return count

def is_valid(board, num, pos):
    # Check row
    if num in board[pos[0]]:
        return False
    
    # Check column
    if num in [board[i][pos[1]] for i in range(len(board))]:
        return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

def mask_grid(board):
    """
    Removes numbers to create a puzzle, checking that a unique solution remains.
    """
    side = 9
    puzzle = [row[:] for row in board]
    
    coords = [(r, c) for r in range(side) for c in range(side)]
    random.shuffle(coords)
    
    # Try to remove numbers one by one
    for r, c in coords:
        original_val = puzzle[r][c]
        puzzle[r][c] = 0  # Temporarily remove
        
        board_copy = [row[:] for row in puzzle]
        if solve_check(board_copy) != 1:
            puzzle[r][c] = original_val  # Put it back if uniqueness is lost
            
    return puzzle

def save_sudoku_image(puzzle, filename):
    fig, ax = plt.subplots(figsize=(7, 7))

    for i in range(10):
        linewidth = 2.5 if i % 3 == 0 else 1.0
        ax.plot([0, 9], [i, i], color='black', linewidth=linewidth)
        ax.plot([i, i], [0, 9], color='black', linewidth=linewidth)

    for r in range(9):
        for c in range(9):
            val = puzzle[r][c]
            if val != 0:
                # Adjusted text position and size: fontsize 20 -> 22
                ax.text(c + 0.5, 8.5 - r, str(val),
                        va='center', ha='center', fontsize=22,
                        weight='bold', family='sans-serif')

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.savefig(filename, bbox_inches='tight', dpi=200, pad_inches=0.2)
    plt.close()

# Execution
full_solution = create_base_grid()

print("GTFA FULL SOLUTION:")
for row in full_solution:
    print(row)

# Now uses the safe masking function
puzzle_state = mask_grid(full_solution)

print("\nGENERATED PUZZLE (Uniquely Solvable):")
for row in puzzle_state:
    print(row)

save_sudoku_image(puzzle_state, "high_complexity_logic_grid.png")
