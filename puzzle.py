from browser import document, window
import random

# State to keep track of the tiles
puzzle_size = 4
puzzle_state = [[] for _ in range(puzzle_size)]

move_count = 0

def increment_move_count():
    global move_count
    move_count += 1
    document['moves'].text = str(move_count)

def reset_move_count():
    global move_count
    move_count = 0
    document['moves'].text = str(move_count)

def find_possible_movements(puzzle):
    # Find the position of the empty tile (0)
    for i, row in enumerate(puzzle):
        for j, value in enumerate(row):
            if value == 0:
                empty_tile_position = (i, j)
                break

    movements = []
    x, y = empty_tile_position
    puzzle_size = len(puzzle)

    # Possible moves: above, below, left, right
    possible_moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    for move_x, move_y in possible_moves:
        if 0 <= move_x < puzzle_size and 0 <= move_y < puzzle_size:
            movements.append(puzzle[move_x][move_y])

    return movements

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

def find_empty_tile_position(puzzle):
    for i, row in enumerate(puzzle):
        for j, value in enumerate(row):
            if value == 0:
                return (i, j)
    return None

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
    puzzle_container = document['puzzle-container']
    numbers = list(range(1, puzzle_size**2))
    random.shuffle(numbers)
    numbers += [0]

    for index, number in enumerate(numbers):
        row = index // puzzle_size
        col = index % puzzle_size
        tile = create_tile(number, row, col)
        puzzle_container <= tile

def run_code(event):
    editor_content = window.editor.getValue()
    try:
        response = exec(editor_content, globals())
    except Exception as e:
        document["console"].value = str(e)
    document["console"].value = str(response)

document["run"].bind("click", run_code)

generate_puzzle()
print(puzzle_state)
movements = find_possible_movements(puzzle_state)
print(movements)
