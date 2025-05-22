# DO NOT modify or add any import statements
#from support import *
#from display import HearthView

# Name:Kenneth Goodall
# Student Number: 4394895
# Favorite Building: 
# -----------------------------------------------------------------------------

# Define your classes and functions here

class Card():
    def __init__(self, **kwargs):
        self._name = kwargs.get('name', 'Card')
        self._symbol = kwargs.get('symbol', 'C')
        self._description = kwargs.get('description', 'A card.')
        self._cost = kwargs.get('cost', 1)
        self._permanent = kwargs.get('permanent', False)
        self._effect = kwargs.get('effect', {})

    def __str__(self):
        return f"{self._name}: {self._description}"

    def __repr__(self):
        return f"{self.__class__.__name__}()"
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
        self._description = f"Cast a protective shield that can absorb {self._strength} damage."
        self._permanent = False
        self._effect = {"shield": self._strength}





class Heal(Card):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name = "Heal"
        self._symbol = "H"
        self._strength = 2
        self._cost = 2
        self._description = f"Cast an aura on target. It recovers {self._strength} health."
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
        self._description = f"{self._name.upper()}! Deals 3 + [turns in hand] damage. Currently dealing {self._strength} damage."
        self._effect = {"damage": self._strength}
    def increment_turn(self):
        self._turns += 1
        self._update_attributes()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._turns})"


class CardDeck():
    def __init__(self, cards: list[Card]):
        """Initialize the deck """
        self._cards = list(cards)

    def __str__(self) -> str:

        return ",".join(card.get_symbol() for card in self._cards)

    def __repr__(self) -> str:
        """Return reconstructable string representation."""
        card_rep =[]
        for card in self._cards:
            if isinstance(card, Fireball):
                card_rep.append(f"{card.__class__.__name__}({card._turns})")

            else:
                card_rep.append(f"{card.__class__.__name__}()")
        return f"CardDeck([{', '.join(card_rep)}])"
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

#Task 6 -- Entity class creation
class Entity():
    def __init__(self, health: int, shield: int):
        self._health = health
        self._shield = shield

    def __str__(self) -> str:
        return f'{self._health},{self._shield}'

    def __repr__(self):
        return f"{self.__class__.__name__}({self._health}, {self._shield})"
    def get_health(self):
        return self._health
    def get_shield(self):
        return self._shield

    def apply_shield(self,shield):
        self._shield = self.get_shield() + shield

    def apply_health(self, health: int):
        self._health = self.get_health() + health

    def apply_damage(self, damage: int):
        dam_list = [1 for _ in range(damage)]
        for i in dam_list:
            if self._shield > 0:
                self._shield += -i
            elif self._health > 0:
                self._health += -i
            else:
                self._health ==0
                break

    def is_alive(self) -> bool:
        if self._health > 0:
             return True
        else:
            return False

class Hero(Entity):
    def __init__(self, health: int, shield: int, max_energy: int, deck: CardDeck, hand: list[Card]):
        super().__init__(health,shield)
        self._health = health
        self._shield = shield
        self._max_energy = max_energy
        self._current_energy = max_energy
        self._deck = deck
        self._hand = hand

    def __str__(self) -> str:
        return (
            f"{self.get_health()},{self.get_shield()},"
            f"{self.get_energy()};"
            f"{str(self._deck)};"
            f"{','.join(c.get_symbol() for c in self._hand)}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self._health}, "
            f"{self._shield}, "
            f"{self._max_energy}, "
            f"{repr(self._deck)}, "
            f"{repr(self._hand)})"
        )

    def get_energy(self):
        return self._current_energy


    def spend_energy(self, energy: int) -> bool:
        if self._current_energy >= energy:
            self._current_energy -= energy
            return True
        return False

    def get_max_energy(self) -> int:
        return self._max_energy

    def get_deck(self) -> CardDeck:
        return self._deck

    def get_hand(self) -> list[Card]:
        return self._hand

    def new_turn(self):
        for card in self._hand:
            if isinstance(card, Fireball):
                card.increment_turn()

        while len(self._hand) <5:
            drawn_cards = self._deck.draw_cards(1)
            if drawn_cards:
                self._hand.extend(drawn_cards)


        if self._max_energy < 10:
            self._max_energy += 1


        self._current_energy = self._max_energy

    def is_alive(self) -> bool:
        if self._health > 0 and not self._deck.is_empty():
             return True
        else:
            return False

class Minion(Card, Entity):

    def __init__(self, health: int, shield: int, **kwargs):
        Card.__init__(self, **kwargs)
        Entity.__init__(self, health, shield)

        self._name = kwargs.get('name', 'Minion')
        self._symbol = kwargs.get('symbol', 'M')
        self._cost = kwargs.get('cost', 2)
        self._description = "Summon a minion."
        self._permanent = True
        self._effect = kwargs.get('effect', {})

        """self._name = 'Minion'
        self._permanent = True
        self._cost =2
        self._strength = 0
        self._symbol ='M'
        self._description = f"{self._name}: Summon a {self._name} "
        self._effect ={}"""


    def __str__(self) -> str:
        return Card.__str__(self)

    def __repr__(self):
        return Entity.__repr__(self)


    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:

        return self

 # Task 9!
class Wyrm(Minion):
    pass




def main() -> None:
    pass

if __name__ == "__main__":
    main()