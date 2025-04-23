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

size = 8
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
    """ produces square board with dimensions size(intger) and fills square with string values of empty board
    corresponding with lower case 'x'. """
    a = [['+' for _ in range(size)] for _ in range(size)]
    print(a)
    return a


def generate_initial_board() -> list[list[str]]:
    """ Takes the board which is list of list filled with strings
    and initialises starting values of 'O' and 'X' """
    a[3][3]='O'
    a[3][4]= 'X'
    a[4][3] ='X'
    a[4][4] ='O'
    print(a)
    return a


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
    """Generates board with indiced placement."""
    board_indices =[[(i, j) for j in range(size)] for i in range(size)] #not needed for this section should move to task 3
    print(board_indices[0][1])
    for i in range((len(position))):
        if position[i] == new_position[i]:# Check to see if on same row
            if i == 0:
                difference = (position[1]-new_position[1])
                for i in range(position[1],new_position[1]-1):
                    k +=1
                    intermediates.append(((position[1]),(position[1]+k)))
                    print(intermediates)

            else :
                for i in range(position[0],new_position[0]-1):
                    k +=1
                    difference = (position[0]-new_position[0])
                    intermediates.append(((position[1]+k),(position[1])))
                    print(intermediates)
                    #working code excluding diagonals
        else:
            print('positions are possibly diagonal of each other')
    return intermediates


move_to_index('Z100')
a =generate_empty_board(size)
generate_initial_board()
board =  [["X","X"],["O","X"]]
check_winner(board)
get_intermediate_locations((0,0),(6,0))

def main() -> None:
    """
    The main function (You should write a better docstring!)
    """
    pass

if __name__ == "__main__":
    main()