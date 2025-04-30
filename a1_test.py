from support import *

def num_hours()-> float:
    days =10
    hours =2.5
    total =days*hours
    return days*hours
def generate_empty_board(size: int) -> list[list[str]]:
    """Produces square board with dimensions size and fills with EMPTY values (+)."""
    return [[EMPTY for _ in range(size)] for _ in range(size)]


def move_to_index(move: str) -> tuple[int,int]:
    mov_index =()
    if 64 < ord(move[0]) < 91:
        index1 =int(ord(move[0])- ord('A'))
        index2 = int(move[1:]) - 1
        mov_index =(index1,index2)
        print(mov_index)
        return mov_index
    else :
        print('Need capital letter')

def index_to_move(index: tuple[int, int]) -> str:
    """Converts (row, column) index positions to alphanumeric notation."""
    row, col = index
    move_char = chr(ord('A') + row)
    move_num = str(col + 1)
    return f"{move_char}{move_num}"



def generate_initial_board() -> list[list[str]]:
    """ Takes the EMPTY board which is list of list filled with strings
    and initialises starting values of 'O' and 'X' """

    board = generate_empty_board(BOARD_SIZE)  # calls earlier function


    board[3][3] = 'O' # fills board postion row 3,column 3 with 'O'
    board[3][4] = 'X'
    board[4][3] = 'X'
    board[4][4] = 'O'

    return board


def check_winner(board: list[list[str]]) -> str:
    x_count = 0
    o_count = 0

    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if element == 'X':
                x_count += 1
            elif element == 'O':
                o_count += 1

    if x_count > o_count:
        print('x')
        return 'X'
    elif o_count > x_count:
        print('O')
        return 'O'
    else:
        return ""

def display_board(board: list[list[str]]):
    """Prints game board with proper formatting."""
    rows = len(board)
    columns = len(board[0])

    # Printing column values with spacing
    header = "  " + "".join(f"{i + 1 :2}" for i in range(columns))
    print(header)

    # Printing top border
    header_2 = "  " + "".join(f'- ' for i in range(columns + 1))
    print(header_2)

    # Printing
    for i in range(rows):
        row_label = chr(ord('A') + i) + VERTICAL_SEPARATOR
        cells = "".join(f"{cell:^2}" for cell in board[i]) + VERTICAL_SEPARATOR
        print(f"{row_label} {cells}")

    # Print bottom border
    print(header_2)


def get_valid_command(valid_moves: list[str]) -> str:
    """Prompts user for valid move."""
    # Add command options to valid moves
    updated_valid_moves = valid_moves.copy()
    updated_valid_moves.extend(['Q', 'H'])

    while True:
        val = input(MOVE_PROMPT).upper()
        if val in updated_valid_moves:
            return val

def get_intermediate_locations(position: tuple[int, int], new_position: tuple[int, int]) -> list[tuple[int, int]]:
    intermediates = []
    """ Generates intermediate positions between 2 chosen positions as long as two positions are either purely 
    horizontal, purely vertical or purely diagonal from one another
     """

    # Check vertical movement (same column)
    if position[1] == new_position[1]:
        step = 1 if new_position[0] > position[0] else -1
        for x in range(position[0] + step, new_position[0], step):
            intermediates.append((x, position[1]))
        return intermediates

    # Check horizontal movement (same row)
    if position[0] == new_position[0]:
        step = 1 if new_position[1] > position[1] else -1
        for y in range(position[1] + step, new_position[1], step):
            intermediates.append((position[0], y))
        return intermediates

    # Diagonal movement utilizing smaller subsection of the matrix
    min_row = min(position[0], new_position[0])
    max_row = max(position[0], new_position[0])
    min_col = min(position[1], new_position[1])
    max_col = max(position[1], new_position[1])
    submatrix_size = max(max_row - min_row, max_col - min_col) + 1

    diagonals = []

    # Main diagonals (top-left to bottom-right)
    # Diagonals starting from left edge
    for d in range(max_col - min_col + 1):
        diagonal = []
        i = min_row
        j = min_col + d
        while i <= max_row and j <= max_col:
            diagonal.append((i, j))
            i += 1
            j += 1
        if diagonal:  # Only add if not empty
            diagonals.append(diagonal)

    # Diagonals starting from top edge (skip first to avoid duplicate)
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

    # Anti-diagonals (top-right to bottom-left)
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

    # Diagonals starting from top edge (skip first to avoid duplicate)
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

    # Check all diagonals for containing both positions
    for diagonal in diagonals:
        if position in diagonal and new_position in diagonal:
            index1 = diagonal.index(position)
            index2 = diagonal.index(new_position)
            start, end = min(index1, index2), max(index1, index2)
            print(diagonal[start +1:end])
            return diagonal[start + 1:end]

    return []


def get_reversed_positions(board: list[list[str]], piece: str, position: tuple[int, int]) -> list[tuple[int, int]]:
    """Returns positions that would be reversed by placing piece at position.
    Utilizes get_intermediate_locations to fill in the needed positions to flip."""
    x, y = position
    size = len(board)

    # Validate position
    if not (0 <= x < size and 0 <= y < size) or board[x][y] != '+':
        return []

    opponent = 'O' if piece == 'X' else 'X'
    reversed_positions = []

    # Check all directions
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        # Find endpoint in this direction
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
    print(sorted(valid_moves))
    return sorted(valid_moves)

def make_move(board: list[list[str]], piece: str, move: str):
    position = move_to_index(move)
    board[position[0]][position[1]] = str(piece)
    display_board(board)     # Need to possibly move this function ahead of display function


def play_a_game():
    """Function to play game of Reversi using all the implemented functions."""
    # Initialize game
    board = generate_initial_board()
    current_player = 'X'
    game_over = False

    print(WELCOME_MESSAGE)
    print(HELP_MESSAGE)
    print(MOVE_PROMPT)

    while not game_over:
        # Display current board state
        display_board(board)

        # Get available moves for current player
        valid_moves = get_available_moves(board, current_player)

        # Check for game end conditions
        if not valid_moves:
            other_player = 'O' if current_player == 'X' else 'X'
            other_moves = get_available_moves(board, other_player)

            if not other_moves:  # Neither player can move
                game_over = True
                break

            print(f"{current_player} has no valid moves. Passing turn to {other_player}.")
            current_player = other_player
            continue

        # Get player move
        print(f"\nPlayer {current_player}'s turn")
        print(f"Available moves: {', '.join(valid_moves)}")
        command = get_valid_command(valid_moves)

        # Handle special commands
        if command == 'Q':
            print("PLAYER quit game.")
            return
        elif command == 'H':
            print(HELP_MESSAGE)
            continue

        # Make the move
        position = move_to_index(command)
        reversed_positions = get_reversed_positions(board, current_player, position)

        # Place the piece and flip opponent pieces
        board[position[0]][position[1]] = current_player
        for (x, y) in reversed_positions:
            board[x][y] = current_player

        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'

    # Game over - determine winner
    display_board(board)
    winner = check_winner(board)
    if winner:
        print(f"\nGame over! Player {winner} wins!")
    else:
        print("\nGame over! It's a tie!")


play_a_game()

