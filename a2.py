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

    def __repr__(self):
        return f"{self.__class__.__name__}"
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
    def __init__(self, cards: list[Card]):
        """Initialize the deck """
        self._cards = list(cards)  # Create a copy to avoid modifying the original list

    def __str__(self) -> str:

        return ",".join(card.get_symbol() for card in self._cards)

    def __repr__(self) -> str:
        """Return reconstructable string representation."""
        card_reprs = [f"{card.__class__.__name__}()" for card in self._cards]
        return f"CardDeck([{', '.join(card_reprs)}])"

    def is_empty(self):
        if len(self._cards) > 0:
            return False
        else:
            return True

    def remaining_count(self) -> int:
        return len(self._cards)

    def draw_cards(self, num: int) -> list[Card]:
        """
        Draws the specified number of cards from the top of the deck.
        Returns cards in the order they were drawn.
        If there aren't enough cards, returns as many as possible.
        """
        drawn = []
        for _ in range(min(num, self.remaining_count())):
            drawn.append(self._cards.pop(0))
        return drawn

    def add_card(self, card: Card):
        """Add a card to the bottom of the deck."""
        self._cards.append(card)
def main() -> None:
    pass

if __name__ == "__main__":
    main()