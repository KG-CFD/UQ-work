# DO NOT modify or add any import statements
from support import *

# Name: Kenneth Goodall
# Student Number: 43948958
# Favorite Marsupial: Platypus
# -----------------------------------------------------------------------------

# Define your functions here (start with def num_hours() -> float)
def num_hours()-> float:
    days =10
    hours =2.5
    total =days*hours
    print('Total hours spent =', total)
    return days*hours

num_hours()

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


move_to_index('H8')

def generate_empty_board(size: int) -> list[list[str]]:
    """ produces square board with dimensions size(intiger) and fills square with string values of empty board
    corresponding with lower case 'x'. """
    a = [[EMPTY for _ in range(size)] for _ in range(size)]
    print(a)
    return a


def generate_initial_board() -> list[list[str]]:
    """ Takes the board which is list of list filled with strings
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


def get_intermediate_locations(position: tuple[int, int], new_position: tuple[int, int]) -> list[tuple[int, int]]:
    intermediates =[]
    k=0
    """ Generates intermediate positions between 2 chosen positions, either vertical,horizontal or diagonal"""
    board_indices =[[(i, j) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)] #not needed for this section should move to task 3
    print(board_indices[0][1])
    for i in range((len(position))):
        if position[i] == new_position[i]:# Check to see if on same row
            if i == 0:
                difference = (position[1]-new_position[1])
                for i in range(position[1],new_position[1]-1):
                    k +=1
                    intermediates.append(((position[0]),(position[1]+k)))
                    print(intermediates)

            else :
                for i in range(position[0],new_position[0]-1):
                    k +=1
                    difference = (position[0]-new_position[0])
                    intermediates.append(((position[0]+k),(position[1])))
                    print(intermediates)
                    #working code excluding diagonals
        else:
            # For the diagonals code finds intermediates by creating smallest
            # submatrix that contains both positions and checking which diagonal it lies on and returning intermediates
            min_row =min(position[0],new_position[0])
            max_row =max(position[0],new_position[0])
            min_col =min(position[1],new_position[1])
            max_col =max(position[1], new_position[1])
            submatrix_size = max(max_row -min_row, max_col -min_col) + 1

            diagonals =[]
            for d in range(submatrix_size):
                diagonal = []
                i =min_row
                j =min_col + d
                while i <= max_row and j <= max_col:
                    diagonals.append((i,j))
                    i += 1
                    j += 1
                diagonals.append(diagonal)

            #case where diagonals are (i+1,j)
            for d in range(1,submatrix_size):
                diagonal =[]
                i =min_row + d




    return intermediates

def display_board(board: list[list[str]]):
    """ Prints game board and shows"""
    rows= len(board)
    columns =len(board[0])

    header = "  " + "".join(f"{i+1 :2}" for i in range(columns))
    print(header)  # prints column headers
    header_2 ="  " + "".join(f'- ' for i in range(columns+1)) #top and bottom edge of board with dashed lines
    print(header_2)
    for i in range(rows):
        row_label = chr(ord('A') + i) + VERTICAL_SEPARATOR
        # Format cells with borders and proper spacing
        cells = "".join(f"{cell:^2}" for cell in board[i]) + VERTICAL_SEPARATOR
        print(f"{row_label} {cells}")
    print(header_2)

def get_valid_command(valid_moves: list[str]) -> str:
    """ Returns all valid moves """
    while True:  # Keep repeating until command satisfied
        val = input(MOVE_PROMPT).upper()
        updated_valid_moves =valid_moves.copy()
        updated_valid_moves.extend(['Q','q','H','h'])
        if val in updated_valid_moves:
            return val


def get_reversed_positions(board: list[list[str]], piece: str) -> list[str]:

    if not board or len(board) != 8 or len(board[0]) != 8:
        return []
    opponent_piece = 'O' if piece == 'X' else 'X'
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    valid_moves = []

    for x in range(8):
        for y in range(8):
            if board[x][y] != '+':
                continue  # Skip occupied positions

            has_valid_move = False

            for dx, dy in directions:
                i, j = x + dx, y + dy
                found_opponent = False

                while 0 <= i < 8 and 0 <= j < 8:
                    if board[i][j] == opponent_piece:
                        found_opponent = True
                        i += dx
                        j += dy
                    elif board[i][j] == piece and found_opponent:
                        # Valid move found
                        has_valid_move = True
                        break
                    else:
                        break  # Empty space or wrong sequence

                if has_valid_move:
                    break  # No need to check other directions

            if has_valid_move:
                row_char = chr(ord('A') + x)
                col_num = y + 1
                valid_moves.append(f"{row_char}{col_num}")
    print(sorted(valid_moves))
    return sorted(valid_moves)


def make_move(board: list[list[str]], piece: str, move: str):
    e = move_to_index(move)
    board[e[0]][e[1]] = str(piece)
    display_board(board)     # Need to possibly move this function ahead of display function







move_to_index('Z100')
a =generate_empty_board(8)
board =generate_initial_board()
check_winner(board)
get_intermediate_locations((5,2),(5,6))
display_board(board)
get_reversed_positions(board , 'X')
make_move(board, "O", "D3")
def main() -> None:
    """
    The main function (You should write a better docstring!)
    """
    pass

if __name__ == "__main__":
    main()
    """ """