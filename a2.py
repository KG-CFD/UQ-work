# DO NOT modify or add any import statements
#from support import *
#from display import HearthView

# Name:Kenneth Goodall
# Student Number: 4394895
# Favorite Building: 
# -----------------------------------------------------------------------------

# Define your classes and functions here

class Card():
    def __init__(self,**kwargs):
        self._name = 'Card'
        self._symbol ='C'
        self._description ="A card."
        self._cost = 1
        self._permanent = False
        self._effect = {}
    def __str__(self):
        return f"{self._name}:{self._description}"

    def get_symbol(self) -> str:
        return self._symbol

    def get_name(self):
        return self._name
    def get_cost(self):
        return self._cost

    def get_effect(self):
        return self._effect

    def is_permanent(self):
        return self._permanent





def main() -> None:
    pass

if __name__ == "__main__":
    main()