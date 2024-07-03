import random

print("""Welcome to the Sliding Puzzle Game!
-----------------------------------
Arrange the 3x3 grid numbers (1-8) in order, with the empty space (0) at the end.
Move tiles by sliding them into the empty space.
Choose four unique letters for the moves: left, right, up, down.
Let's play!""")

def get_move_keys():

    """
        Prompts the user to enter four unique letters to represent the moves: left, right, up, and down.
        Validates that the input consists of exactly four unique, alphabetic characters.
        Output:
        - Returns a dictionary mapping 'left', 'right', 'up', 'down' to the user's chosen letters.
        """

    while True:
        input_str = input("Enter 4 letters for left, right, up, and down moves (e.g., 'l r u d'): ").lower()
        normalized_input = ''.join(input_str.split())
        if len(normalized_input) != 4:
            print("Invalid input: Please enter exactly 4 letters. Try again.")
            continue
        if not normalized_input.isalpha():
            print("Invalid input: Please use only letter characters (a-z). Try again.")
            continue
        if len(set(normalized_input)) != 4:
            print("Invalid input: Please ensure all four letters are unique. Try again.")
            continue
        return {
            'left': normalized_input[0],
            'right': normalized_input[1],
            'up': normalized_input[2],
            'down': normalized_input[3]
        }

def random_puzzle(locations):

    """
        Generates a random, solvable puzzle state for the sliding puzzle game.
        This is achieved by ensuring the number of inversions is even (necessary condition for a solvable 3x3 puzzle).
        Input:
        - locations: A list of integers representing the initial state of the puzzle.
        Output:
        - A list representing a solvable puzzle state.
        """

    random.shuffle(locations)
    while True:
        count = 0
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                if locations[i] > locations[j] and locations[j] != 0:
                    count += 1
        if count % 2 == 0 and count != 0:
            break
        random.shuffle(locations)
    return locations

def available_moves(index_blank, move_keys):

    """
        Determines the available moves based on the position of the blank space.
        Input:
        - index_blank: The index of the blank space in the puzzle.
        - move_keys: A dictionary mapping 'left', 'right', 'up', 'down' to the user's chosen letters.
        Output:
        - A list of moves that are possible from the current state of the puzzle.
        """

    moves = []
    row, col = divmod(index_blank, 3)
    if row < 2: moves.append(('up', move_keys['up']))
    if row > 0: moves.append(('down', move_keys['down']))
    if col < 2: moves.append(('left', move_keys['left']))
    if col > 0: moves.append(('right', move_keys['right']))
    return moves

def move_blank(movement, locations, move_keys):

    """
        Executes a move operation by swapping the blank with the adjacent tile in the specified direction.
        Input:
        - movement: The user's input corresponding to the move direction.
        - locations: A list representing the current state of the puzzle.
        - move_keys: A dictionary mapping directions to user-specified keys.
        Output:
        - Boolean value indicating whether the move was successfully executed.
        """

    index_blank = locations.index(0)
    allowed_moves = available_moves(index_blank, move_keys)
    move_directions = {'up': 3, 'down': -3, 'left': 1, 'right': -1}
    for direction, key in allowed_moves:
        if movement == key:
            locations[index_blank], locations[index_blank + move_directions[direction]] = locations[
                index_blank + move_directions[direction]], locations[index_blank] #change the position
            return True
    return False

def print_puzzle(locations):

    """
       Prints the current state of the puzzle in a 3x3 grid format.
       Input:
       - locations: A list of integers representing the current state of the puzzle.
       """

    print()
    for i in range(len(locations)):
        if locations[i] == 0:
            print(' ', end=' ')
        else:
            print(locations[i], end=' ')
        if (i + 1) % 3 == 0:
            print()
    print()

def play_game(locations, move_keys):

    """
        Manages the game loop, processing user moves and checking for game completion.
        Input:
        - locations: A list representing the initial state of the puzzle.
        - move_keys: A dictionary mapping 'left', 'right', 'up', 'down' to the user's chosen letters.
        """

    step = 0
    completed_sequence = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while locations != completed_sequence:
        print_puzzle(locations)
        index_blank = locations.index(0)
        allowed_moves = available_moves(index_blank, move_keys)
        move_options = ', '.join([f"{direction}-{key}" for direction, key in allowed_moves])

        valid_move_made = False
        while not valid_move_made:
            move = input(f"Enter your move ({move_options}) > ").lower()
            if move in [key for _, key in allowed_moves]:
                if move_blank(move, locations, move_keys):
                    step += 1
                valid_move_made = True
            else:
                print("Invalid move. Please enter one of the correct move keys.")
    print_puzzle(locations)
    print(f"Congratulations! You solved the puzzle in {step} moves!")

def play_again_prompt():

    """
        Prompts the user to decide whether to play another game or to quit.
        Output:
        - Boolean value indicating whether the user wants to quit ('True' to quit).
        """

    while True:
        play_again = input("Enter “n” for another game, or “q” to end the game >  ").strip().lower()
        if play_again == "n":
            return False
        elif play_again == "q":
            return True
        else:
            print("Invalid input. Please enter 'n' or 'q'.")

def play_sliding_puzzle():

    """
        Initializes the game and manages game rounds based on the player's choice to continue playing or to quit.
        """

    move_keys = get_move_keys()
    print("Your chosen move keys:", move_keys)
    while True:
        locations = random_puzzle(list(range(9)))
        play_game(locations, move_keys)
        if play_again_prompt():
            print("Thank you for playing!")
            break

play_sliding_puzzle()
