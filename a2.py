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

class Shield(Card):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name = "Shield"
        self._symbol = "S"
        self._strength = 5
        self._cost = 1
        self._description = f" Cast a protective shield that can absorb {self._strength} damage. "
        self._permanent = False
        self._effect = {"defense": self._strength}





class Heal(Card):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name = "Heal"
        self._symbol = "H"
        self._strength = 2
        self._cost = 2
        self._description = f" Cast an  aura on target. It recovers {self._strength} health."
        self._permanent = False
        self._effect = {"health": self._strength}


class Fireball(Card):
    def __init__(self, turns_in_hand, **kwargs):
        super().__init__(**kwargs)
        self._name = "Fireball"
        self._turns =turns_in_hand
        self._update_attributes()
        self._cost = 3
        self._permanent = False

    def _update_attributes(self):
        self._strength = 3 + self._turns
        self._symbol = str(self._turns)
        self._description = f" Deals 3 + [turns in hand] damage. Currently dealing {self._strength} damage."
        self._effect = {"damage": self._strength}
    def increment_turn(self):
        self._turns += 1
        self._update_attributes()


class CardDeck():
     def _init__(self, cards: list[Card]):










def main() -> None:
    pass

if __name__ == "__main__":
    main()