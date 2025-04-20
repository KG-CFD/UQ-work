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
    if 64 < ord(move[0]) < 73 and int(move[1]) < 9:
        index1 =int(ord(move[0])- ord('A'))
        index2 = int(move[1]) - 1
        mov_index =(index1,index2)
        print(mov_index)
        return mov_index
    else :
        print('Invalid move, make sure indexing is within range (A-H and 1-8)')


move_to_index('H8')

 def generate_empty_board(size: int) -> list[list[str]]:
     """ produces square board with dimensions size(intger) and fills square with string values of empty board
     corresponding with lower case 'x'. """
     i_range,j_range= size -1, size -1
     for i in range(size):    # indexing board
         for j in range(size):





def main() -> None:
    """
    The main function (You should write a better docstring!)
    """
    pass

if __name__ == "__main__":
    main()