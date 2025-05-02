# DO NOT modify or add any import statements
from support import *

# Name: Kenneth Goodall
# Student Number: 43948958
# Favorite Marsupial: Platypus
# -----------------------------------------------------------------------------

# Define your functions here (start with def num_hours() -> float)
def num_hours()-> float:
    days =15
    hours =1.3
    total =days*hours
    return days*hours



def move_to_index(move: str) -> tuple[int,int]:
    """ Takes move from Alphanumeric to plain numerical indexing in doing so it takes arguments of string type
    and returns tuple
      example:   'A2' ----->   (0,3)               """
    mov_index =()
    if 64 < ord(move[0]) < 91:
        index1 =int(ord(move[0])- ord('A'))
        index2 = int(move[1:]) - 1
        mov_index =(index1,index2)
        return mov_index
    else :
        print('Need capital letter')

def index_to_move(index: tuple[int, int]) -> str:
    """Converts (row, column) index positions to alphanumeric notation."""
    row, col = index
    move_char = chr(ord('A') + row)
    move_num = str(col + 1)
    return f"{move_char}{move_num}"
move_to_index('H8')

def generate_empty_board(size: int) -> list[list[str]]:
    """ produces square board with dimensions size(intiger) and fills square with string values of empty board
    corresponding with lower case 'x'. """
    a = [[EMPTY for _ in range(size)] for _ in range(size)]
    return a


def generate_initial_board() -> list[list[str]]:

    """ Takes the board which is a list of lists filled with strings and initialises
    starting board values of 'O' and 'X' """
    board = generate_empty_board(BOARD_SIZE)  # calls earlier function


    board[3][3] = 'O'
    board[3][4] = 'X'
    board[4][3] = 'X'
    board[4][4] = 'O'

    return board


def check_winner(board: list[list[str]]) -> str:
    """ Function returns winner of the game board according to reversi logic where who has most pieces wins."""
    x_count = 0
    o_count = 0

    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if element == 'X':
                x_count += 1
            elif element == 'O':
                o_count += 1

    if x_count > o_count:
        return 'X'
    elif o_count > x_count:
        return 'O'
    else:
        return ""


def get_intermediate_locations(position: tuple[int, int], new_position: tuple[int, int]) -> list[tuple[int, int]]:
    """ generates intermediate positions between 2 chosen positions,either vertical,horizontal or diagonal """
    intermediates = []


    # Check if both  positions are in same column(Vertical)
    if position[1] == new_position[1]:
        step = 1 if new_position[0] > position[0] else -1
        for x in range(position[0] + step, new_position[0], step):
            intermediates.append((x, position[1]))
        return intermediates

    # Check if positions are in same row (Horizontal)
    if position[0] == new_position[0]:
        step = 1 if new_position[1] > position[1] else -1
        for y in range(position[1] + step, new_position[1], step):
            intermediates.append((position[0], y))
        return intermediates

    # Need to now check diagonals
    # Method used creates all diagonals of smallest submatrix that has both position and new_position inside
    # and then checks if both new_position and position are within any diagonals.
    min_row = min(position[0], new_position[0])
    max_row = max(position[0], new_position[0])
    min_col = min(position[1], new_position[1])
    max_col = max(position[1], new_position[1])

    diagonals = []

    # Main diagonals (top-left to bottom-right)
    # Diagonals starting from  bottom left edge
    for d in range(max_col - min_col + 1):
        diagonal = []
        i = min_row
        j = min_col + d
        while i <= max_row and j <= max_col:
            diagonal.append((i, j))
            i += 1
            j += 1
        if diagonal:
            diagonals.append(diagonal)

    # Diagonals starting from top edge
    for d in range(1, max_row - min_row + 1):
        diagonal = []
        i = min_row + d
        j = min_col
        while i <= max_row and j <= max_col:
            diagonal.append((i, j))
            i += 1
            j += 1
        if diagonal:
            diagonals.append(diagonal)

    # Anti-diagonals
    # Diagonals starting from right edge
    for d in range(max_col - min_col + 1):
        diagonal = []
        i = min_row
        j = max_col - d
        while i <= max_row and j >= min_col:
            diagonal.append((i, j))
            i += 1
            j -= 1
        if diagonal:
            diagonals.append(diagonal)

    # Diagonals starting from top edge
    for d in range(1, max_row - min_row + 1):
        diagonal = []
        i = min_row + d
        j = max_col
        while i <= max_row and j >= min_col:
            diagonal.append((i, j))
            i += 1
            j -= 1
        if diagonal:
            diagonals.append(diagonal)

    # Checks all diagonals for having both positions
    for diagonal in diagonals:
        if position in diagonal and new_position in diagonal:
            index1 = diagonal.index(position)
            index2 = diagonal.index(new_position)
            start, end = min(index1, index2), max(index1, index2)
            return diagonal[start + 1:end]

    return []

def display_board(board: list[list[str]]):
    """Prints game board graphically"""

    rows = len(board)
    cols = len(board[0])

    # Print column numbers
    print("  " + "".join(f"{i + 1:1}" for i in range(cols)))

    # Print top border
    print("  " + "-" * (cols ))

    # Print each row
    for i in range(rows):

        cells = "".join(board[i])
        print(f"{chr(ord('A') + i)}|{cells}|")

    # Print bottom
    print("  "+ HORIZONTAL_SEPARATOR * (cols ))

def get_valid_command(valid_moves: list[str]) -> str:
    """ Prompts user for a valid move whereby valid moves include extended list of ['Q','q','H','h'] """

    while True:  # Keep repeating until command satisfied
        val = input(MOVE_PROMPT).upper()
        updated_valid_moves =valid_moves.copy()
        updated_valid_moves.extend(['Q','q','H','h'])
        if val in updated_valid_moves:
            return val


def get_reversed_positions(board: list[list[str]], piece: str, position: tuple[int, int]) -> list[tuple[int, int]]:
    """Returns positions that would be reversed by placing piece at position.
    Utilizes get_intermediate_locations to fill in the needed positions to flip.
    Args:
        board: List[list[str]] representing  game board.
        piece: The piece being placed .
        position: (row, column) coordinates where the piece is placed.

    Returns:
        [(row,column)] positions that would be flipped if the piece is placed"""
    x, y = position
    size = len(board)

    opponent = 'O' if piece == 'X' else 'X'
    reversed_positions = []
    # Code utilizes idea of a sandwich, whereby it searches for player 2s pieces sandwiched between player 1s pieces
    # Checking all directions
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        i, j = x + dx, y + dy

        if not (0 <= i < size and 0 <= j < size and board[i][j] == opponent):
            continue

        # Continue walk in this direction until we find  piece
        while 0 <= i < size and 0 <= j < size and board[i][j] == opponent:
            i += dx
            j += dy

        # If we found our piece at the end, get the intermediate positions
        if 0 <= i < size and 0 <= j < size and board[i][j] == piece:
            # Use get_intermediate_locations to find positions to flip
            positions_to_flip = get_intermediate_locations(position, (i, j))
            reversed_positions.extend(positions_to_flip)

    return reversed_positions




def get_available_moves(board: list[list[str]], player: str) -> list[str]:
    """Returns all valid moves for the given player."""
    size = len(board)
    valid_moves = []

    # Check all empty positions
    for i in range(size):
        for j in range(size):
            if board[i][j] == '+':  # Empty position
                # Need to test wether placing at [i][j] would flip any opponents pieces
                if get_reversed_positions(board, player, (i, j)):
                    valid_moves.append(index_to_move((i, j)))

    return sorted(valid_moves)

def make_move(board: list[list[str]], piece: str, move: str):
    """Updates board with the new piece placement,flipping the required pieces if sandwiched pieces exist  """

    position = move_to_index(move)
    x, y = position
    board[x][y] = piece  # Place the piece

    # Get all opponent pieces to flip
    opponent = 'O' if piece == 'X' else 'X'
    positions_to_flip = get_reversed_positions(board, piece, position)

    # Flip all sandwiched opponent pieces to the current player's color
    for (i, j) in positions_to_flip:
        board[i][j] = piece




def play_game():
    """Function to play game of Reversi with exact output formatting."""
    # Initialize game
    board = generate_initial_board()
    current_player = 'O'  # Player 1
    game_over = False
    pass_count = 0

    print(WELCOME_MESSAGE)

    while not game_over:
        # Display board
        display_board(board)

        # Print whose turn it is
        player_name = "Player 1" if current_player == 'O' else "Player 2"
        print(f"{player_name} to move")

        # Get available moves
        valid_moves = get_available_moves(board, current_player)

        if not valid_moves:
            print(f"{player_name} has no possible move!")
            pass_count += 1

            if pass_count >= 2:
                game_over = True
                break

            current_player = 'X' if current_player == 'O' else 'O'
            continue

        pass_count = 0

        # Get and process move
        print(f"Possible moves: {','.join(valid_moves)}")
        command = get_valid_command(valid_moves)

        if command == 'Q':
            winning_player = "Player 1" if current_player == 'X' else "Player 2"
            print(f"{winning_player} Wins!")
        elif command == 'H':
            print(HELP_MESSAGE)
            continue

        # Make the move
        position = move_to_index(command)
        reversed_positions = get_reversed_positions(board, current_player, position)
        board[position[0]][position[1]] = current_player
        for (x, y) in reversed_positions:
            board[x][y] = current_player

        current_player = 'X' if current_player == 'O' else 'O'

    # Game over - determine winner
    winner = check_winner(board)
    if winner == 'O':
        print("Player 1 Wins!")
    elif winner == 'X':
        print("Player 2 Wins!")
    else:
        print(DRAW_TEXT)
        print(PLAY_AGAIN_PROMPT)








def main() -> None:
    """Runs the game and handles replay functionality
     1. Calls to play game
     2 At end of game prompts player/s to play again
     3 Plays another round or exits when player declines"""

    while True:
        play_game()

        print(PLAY_AGAIN_PROMPT, end='')
        if input().strip().upper() != 'Y':
            print("Cheers for playing!")
            break


if __name__ == "__main__":
    main()
    """ """