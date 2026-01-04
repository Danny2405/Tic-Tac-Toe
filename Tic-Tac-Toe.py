import random


"""
Context: I built this project after earning my PCEP certification and during my
PCAP Python Essentials 2 | PCAP-31-03 training. Please don’t be too harsh if the
form or style isn’t fully “professional” — my goal was to practice with a small,
scientifically inspired project.

Goal:
Build a complete console Tic-Tac-Toe game allowing:
- two human players to play against each other,
- or one human player to play against a random computer.
"""

############################################
# Project: Tic-Tac-Toe (console version)   #
############################################

# -----------------------------
# Part I — Board initialization
# -----------------------------

def initial_area(y, x):
    """Create an empty y×x board filled with spaces."""
    board = [[" " for i in range(x)] for j in range(y)]
    return board


# Global game board (3x3)
area_i = initial_area(3, 3)


def suitable_output(matrix):
    """Display the board in a readable console format."""
    print("-" * 5)
    for i in range(3):
        print("|".join(matrix[i]))
        print("-" * 5)  # Purely for visual aesthetics


# -----------------------------
# Input validation utility
# -----------------------------

def read_int(prompt, mini, maxi):
    """
    Read an integer from the user within [mini, maxi].
    Uses exceptions to handle invalid input robustly.
    """
    while True:
        try:
            text = input(prompt).strip()

            # Empty input is not allowed
            if text == "":
                raise ValueError("empty input")

            # Convert to int (supports +, -, digits)
            value = int(text)

            # Range check
            if not (mini <= value <= maxi):
                raise ValueError("out of range")

            return value

        except ValueError as err:
            # Provide user-friendly feedback depending on the error type
            if str(err) == "empty input":
                print("Error: empty input.")
            elif str(err) == "out of range":
                print(f"Error: the value {value} is not within the permitted range [{mini}, {maxi}].")
            else:
                print("Error: wrong input (please enter a valid integer).")


# -----------------------------
# Game mechanics helpers
# -----------------------------

def valid_coup(board_initial):
    """
    Return a list of all empty cells on the board.
    Each cell is returned as a tuple (row, col).
    """
    list_empty = []
    for i in range(3):
        for j in range(3):
            if board_initial[j][i] == " ":
                list_empty.append((j, i))
    return list_empty


def victory_check(board_initial, symbole):
    """
    Check if the given 'symbole' has a winning line:
    - 3 in a row (any row)
    - 3 in a column (any column)
    - 3 on a diagonal
    """
    list_diagonal = [board_initial[i][i] for i in range(3)]
    list_diagonal_inv = [board_initial[i][2 - i] for i in range(3)]
    symbole_list = [symbole for j in range(3)]

    if (
        list_diagonal == symbole_list
        or list_diagonal_inv == symbole_list
        or any([board_initial[i] == symbole_list for i in range(3)])
        or any([[board_initial[i][j] for i in range(3)] == symbole_list for j in range(3)])
    ):
        return "win"
    else:
        return "continue the game"


# -----------------------------
# Human move (player input)
# -----------------------------

def principal_game_loop(board_initial, symbole):
    """
    Handle one human move:
    - ask for coordinates
    - validate the move
    - update the board
    - check win/draw
    """
    # Ask the player for coordinates
    y_user = read_int("Enter a row number in [0-2] : ", 0, 2)
    x_user = read_int("Enter a column number in [0-2] : ", 0, 2)

    # Check if the chosen cell is empty
    if (y_user, x_user) in valid_coup(board_initial):
        # Place the symbol on the board
        board_initial[y_user][x_user] = symbole

        # If no one wins, the game continues (unless it's a draw)
        if victory_check(board_initial, symbole) == "continue the game":
            suitable_output(board_initial)

            # If there are no more valid moves, it's a draw
            if valid_coup(board_initial) == []:
                print("It's a draw!")
                return False
            else:
                return True  # signal: game continues

        # If player wins
        elif victory_check(board_initial, symbole) == "win":
            suitable_output(board_initial)
            print(f"Congratulations! Player {symbole} wins the game.")
            return False

    else:
        # Cell already taken → ask again
        print("This cell is already occupied. Please choose another one.")
        return principal_game_loop(board_initial, symbole)


# -----------------------------
# Computer move (random choice)
# -----------------------------

def computer_coup(board_initial, symbole):
    """
    Computer chooses a random valid move, plays it, then checks win/draw.
    """
    (y_user, x_user) = random.choice(valid_coup(board_initial))  # chosen coordinates
    board_initial[y_user][x_user] = symbole

    if victory_check(board_initial, symbole) == "continue the game":
        suitable_output(board_initial)

        if valid_coup(board_initial) == []:
            print("It's a draw!")
        else:
            return True  # signal: game continues

    elif victory_check(board_initial, symbole) == "win":
        suitable_output(board_initial)
        print("GAME OVER! You lose.")


# -----------------------------
# Game mode: 1 player vs computer OR 2 players
# -----------------------------

def onevsone_cptvsone(symbole_1, symbole_2, number_of_player):
    """
    Main game loop depending on the chosen mode:
    - 1 player: human vs random computer
    - 2 players: human vs human
    """
    if number_of_player == 1:
        print(f"OK! You chose to play against the computer. Your symbol is: {symbole_1}")

        while True:
            print(f"\nPlayer {symbole_1}")
            if principal_game_loop(area_i, symbole_1):
                print("\nComputer")
                if computer_coup(area_i, symbole_2):
                    continue
                else:
                    break
            else:
                break

    if number_of_player == 2:
        print(f"OK! Two-player mode: Player {symbole_1} vs Player {symbole_2}")

        while True:
            print(f"\nPlayer {symbole_1}")
            if principal_game_loop(area_i, symbole_1):
                print(f"\nPlayer {symbole_2}")
                if principal_game_loop(area_i, symbole_2):
                    continue
                else:
                    break
            else:
                break


# -----------------------------
# Program entry point
# -----------------------------

first_question = read_int(
    "How many players will play this game ? Enter 1 (Player X vs Computer) or 2 (Player X vs Player 0): ",
    1,
    2
)
onevsone_cptvsone("X", "0", first_question)
