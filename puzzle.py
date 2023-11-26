from copy import copy
from browser import document, window
import random

# State to keep track of the tiles
puzzle_size = 4
puzzle_state = [[] for _ in range(puzzle_size)]
goal_state = []

move_count = 0

def get_puzzle_state():
    return puzzle_state

def get_puzzle_size():
    return puzzle_size

def get_goal_state():
    return goal_state

def increment_move_count():
    global move_count
    move_count += 1
    document['moves'].text = str(move_count)

def reset_move_count():
    global move_count
    move_count = 0
    document['moves'].text = str(move_count)

def find_empty_tile_position(puzzle):
    for i, row in enumerate(puzzle):
        for j, value in enumerate(row):
            if value == 0:
                return (i, j)
    return None

def find_possible_movements(puzzle):
    # Find the position of the empty tile (0)

    movements = []
    x, y = find_empty_tile_position(puzzle)
    puzzle_size = len(puzzle)

    # Possible moves: above, below, left, right
    possible_moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    for move_x, move_y in possible_moves:
        if 0 <= move_x < puzzle_size and 0 <= move_y < puzzle_size:
            movements.append(puzzle[move_x][move_y])

    return movements

def swap_and_reconstruct(puzzle, element1, element2):
    """
    Flattens the puzzle, swaps two elements, and reconstructs it back to 2D.

    :param puzzle: 2D list representing the puzzle.
    :param element1: First element to swap.
    :param element2: Second element to swap.
    :return: New puzzle with elements swapped.
    """
    size = len(puzzle)
    flat_puzzle = [item for row in puzzle for item in row]

    # Find indices of the elements
    try:
        index1 = flat_puzzle.index(element1)
        index2 = flat_puzzle.index(element2)
    except ValueError:
        return "One or both elements not found in the puzzle"

    # Swap the elements
    flat_puzzle[index1], flat_puzzle[index2] = flat_puzzle[index2], flat_puzzle[index1]

    # Reconstruct the puzzle back to 2D
    return flat_puzzle


def create_tile(number, row, col):
    tile = document.createElement('div')
    tile.className = 'puzzle-tile'
    if not number:
        tile.classList.add('empty')
        tile.text = ''
    else:
        tile.text = str(number)
    tile.bind('click', on_tile_click)
    tile.id = f'tile-{row}-{col}'
    puzzle_state[row].append(number)
    return tile

def on_tile_click(event):
    tile_number = event.target.text
    movements = find_possible_movements(puzzle_state)
    if tile_number and int(tile_number) in movements:
        move_tile(event.target)

def move_tile(clicked_tile):
    empty_row, empty_col = find_empty_tile_position(puzzle_state)
    clicked_row, clicked_col = map(int, clicked_tile.id.split('-')[1:])

    # Calculate the translation distance for the animation
    translate_x = (empty_col - clicked_col) * 100  # Adjust multiplier based on tile size and grid gap
    translate_y = (empty_row - clicked_row) * 100

    # Apply the transformation
    clicked_tile.style.transform = f'translate({translate_x}%, {translate_y}%)'

    # Function to update the state and UI after the animation
    def update_state():
        # Swap tiles in the puzzle state
        puzzle_state[empty_row][empty_col], puzzle_state[clicked_row][clicked_col] = \
        puzzle_state[clicked_row][clicked_col], puzzle_state[empty_row][empty_col]

        increment_move_count()

        # Update the UI
        update_puzzle_ui()

        # Reset the transformation
        clicked_tile.style.transform = ''

    # Set a timeout to update the state and UI after the animation completes
    window.setTimeout(update_state, 200) 

def update_puzzle_ui():
    for row in range(puzzle_size):
        for col in range(puzzle_size):
            tile_number = puzzle_state[row][col]
            tile = document[f'tile-{row}-{col}']
            tile.text = str(tile_number) if tile_number != 0 else ''
            if tile_number == 0:
                tile.classList.add('empty')
            else:
                tile.classList.remove('empty')

def generate_puzzle():
    global goal_state
    puzzle_container = document['puzzle-container']
    puzzle_container.clear()  # Clear existing tiles

    numbers = list(range(1, puzzle_size**2))
    goal_state = copy(numbers) + [0]
    random.shuffle(numbers)
    numbers += [0]

    for index, number in enumerate(numbers):
        row = index // puzzle_size
        col = index % puzzle_size
        tile = create_tile(number, row, col)
        puzzle_container <= tile
    
    print(puzzle_state)
    movements = find_possible_movements(puzzle_state)
    print(movements)

def print_to_console(text):
    document["console"].value = text

def run_code(event):
    editor_content = window.editor.getValue()
    try:
        response = exec(editor_content, globals())
        if response:
            print_to_console(str(response))
    except Exception as e:
        print_to_console(str(e))

def update_puzzle_size(event):
    global puzzle_size, puzzle_state

    puzzle_size = int(document['puzzle-size-selector'].value)
    puzzle_state = [[] for _ in range(puzzle_size)]
    reset_move_count()
    generate_puzzle()

    # Update the grid layout
    puzzle_grid = document['puzzle-container']
    puzzle_grid.style.gridTemplateColumns = ' '.join(['1fr' for _ in range(puzzle_size)])

    # Dynamically adjust tile size and font
    base_tile_size = 100  # Base size for 4x4 puzzle
    base_font_size = 40  # Base font size for 4x4 puzzle
    scale_factor = 4 / puzzle_size  # Adjust according to the base size

    tile_size = base_tile_size * scale_factor
    font_size = base_font_size * scale_factor

    for tile in document.select('.puzzle-tile'):
        tile.style.height = f'{tile_size}px'
        tile.style.fontSize = f'{font_size}px'


# Bind update_puzzle_size to the dropdown's change event
document['puzzle-size-selector'].bind('change', update_puzzle_size)

document["run"].bind("click", run_code)
generate_puzzle()