import turtle
import numpy as np
import random


background_color = "white"
text_color = "blue"
tile_color = "pale green"
empty_color = "white"
complete_color = "red"

puzzle = None
size = 0


def random_puzzle(size,locations):
    """
    Generates a solvable puzzle of a given size.
    This function ensures the generated puzzle is solvable by checking the parity of
    inversions and, for even-sized boards, the row of the blank space from the bottom.
    """
    # Generate a random sequence of tiles
    random.shuffle(locations)

    while True:
        count = 0  # Initialize inversion count

        # Count inversions in the sequence
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                if locations[i] > locations[j] and locations[j] != 0:
                    count += 1

        # Calculate the row of the blank space from the bottom (1-indexed)
        blank_row_from_bottom = size - (locations.index(0) // size)
        if size % 2 == 1:  # For odd-sized puzzles
            if count % 2 == 0:  # Solvable if inversions are even
                break
        else:  # For even-sized puzzles
            if (count + blank_row_from_bottom) % 2 == 1:  # Solvable if sum is odd
                break
        random.shuffle(locations)  # Shuffle and try again if not solvable
    return np.array(locations).reshape((size, size))

def draw_puzzle():

    """. Clears the turtle screen and redraws the entire puzzle
    based on the current state ofthe puzzle matrix.
    It iterates through the puzzle matrix and draws each tile using draw_tile function."""

    global puzzle, size
    turtle.clear()
    for i in range(size):
        for j in range(size):
            draw_tile(j, i, puzzle[i, j])
    turtle.update()

def draw_tile(col, row, number, show_number=True):

    """
    Draws a single tile at the specified column and row.
    show number = true means I can generate tile without number
    """

    global size, tile_color, empty_color, text_color
    tile_size = 80
    gap = 5
    x = col * (tile_size + gap) - (size * tile_size + (size - 1) * gap) / 2
    y = (size * tile_size + (size - 1) * gap) / 2 - row * (tile_size + gap)
    turtle.penup()
    turtle.goto(x, y)
    turtle.fillcolor(tile_color if number else empty_color)
    turtle.begin_fill()

    for _ in range(4):
        turtle.forward(tile_size)
        turtle.right(90)
    turtle.end_fill()

    if number and show_number:
        draw_number(x + tile_size / 2, y - tile_size / 2, number)


def draw_number(x, y, number):
    """
    Draws the number on the tile.To haddle the number “reoccurance"
    """
    turtle.goto(x, y - 10)
    turtle.color(text_color)
    turtle.write(number, align="center", font=("Arial", 18, "normal"))

def is_complete():
    """Checks if the puzzle is completed."""
    global puzzle, size
    expected = list(range(1, size**2)) + [0]
    flat_puzzle = [item for sublist in puzzle for item in sublist]
    if flat_puzzle == expected:
        show_completion()

def show_completion():

    """
    Handles the movement of tiles when a tile is clicked.
    If the clicked tile is adjacent to the empty tile, it moves the clicked tile into the empty space.
    Args:
        """

    global puzzle, tile_color, size
    tile_color = complete_color
    draw_puzzle()
    turtle.penup()
    turtle.hideturtle()
    screen = turtle.Screen()
    screen.onscreenclick(None)

def on_click(x, y):
    """Handles tile movement on click."""
    global puzzle, size
    col = int((x + size * 80 / 2) // 80)
    row = int((size * 80 / 2 - y) // 80)
    empty_row, empty_col = np.where(puzzle == 0)[0][0], np.where(puzzle == 0)[1][0]
    if abs(col - empty_col) + abs(row - empty_row) == 1:
        animate_movement((col, row), (empty_col, empty_row), number=puzzle[row][col])
        puzzle[empty_row][empty_col], puzzle[row][col] = puzzle[row][col], 0
        draw_puzzle()
        is_complete()

def animate_movement(start, end, number):

    """
    Animates the movement of a tile from its current position to the empty position.
    Args:
    - start: A tuple containing the starting coordinates of the tile.
    - end: A tuple containing the ending coordinates of the tile.
    - number: The number on the moving tile.
    """

    global size
    screen = turtle.Screen()
    screen.onscreenclick(None)#forbid click during the movement
    steps = 80
    start_x, start_y = start
    end_x, end_y = end
    dx = (end_x - start_x) * 80 / steps
    dy = (end_y - start_y) * 80 / steps
    for i in range(steps):
        draw_tile(start_x, start_y, 0, show_number=False)
        start_x += dx / 80
        start_y += dy / 80
        draw_tile(start_x, start_y, number, show_number=False)
        turtle.update()
        turtle.speed(1)
        turtle.delay(100)

    draw_tile(end_x, end_y, number)
    screen.onscreenclick(on_click)#re-allow the click

def start_game():

    """Sets up the game and starts the main loop."""

    global puzzle, size
    size = int(turtle.numinput("Sliding Puzzle", "Puzzle Dimension:", minval=3, maxval=5))
    if size is None:
        turtle.bye()
        return
    screen = turtle.Screen()

    screen.setup(size * 80 + 20, size * 80 + 20)
    screen.bgcolor(background_color)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.tracer(0, 0)
    locations = list(range(size**2))
    puzzle = random_puzzle(size, locations)
    draw_puzzle()
    screen.onscreenclick(on_click)
    turtle.done()

try:
    start_game()
except Exception as e:#make it robust
    print(f"An error occurred during game setup or execution: {e}")