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
        for card in self._cards:   # This is messy should redo to keep encapsulation. (Need to add __repr__  to Fireball)
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
    def __init__(self,health, shield, **kwargs):
        super().__init__(health, shield,**kwargs)
        self._name = "Wyrm"
        self._symbol = "W"
        self._strength = {}
        self._cost = 2
        self._shield = shield
        self._health = health
        self._description = f"{self.__class__.__name__}: Summon a Mana {self.__class__.__name__} to buff your minions."
        self._permanent = True
        self._effect = {"health": 1, "shield": 1 }

    def __str__(self):
        return self._description

    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity],
                      enemy_minions: list[Entity]) -> Entity:
        # Need to return ally_hero or ally_minion  with lowest health
        potential_targets = [ally_hero] + ally_minions

        # Find minimum health value among targets
        min_health = min(target.get_health() for target in potential_targets)

        # Get all targets with min health
        min_health_targets = [target for target in potential_targets
                              if target.get_health() == min_health]


        if ally_hero in min_health_targets:
            return ally_hero
        else:

            for minion in ally_minions:
                if minion.get_health() == min_health:
                    return minion


class Raptor(Minion):
    def __init__(self,health, shield, **kwargs):
        super().__init__(health, shield,**kwargs)
        self._name = "Raptor"
        self._symbol = "R"
        self._health = health
        self._shield =shield
        self._cost = 2
        self._strength = health
        self._effect = {'damage': self._health}
        self._description = f"Summon a Bloodfen {self._name} to fight for you."

    def apply_health(self, health: int):
        """Overring apply_health in Card class"""
        super().apply_health(health)
        super().apply_damage(health)
        self._strength = self._health
        self._effect['damage'] = self._health  # Update damage effect


    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity],
                      enemy_minions: list[Entity]) -> Entity:
        healths=[]
        if len(enemy_minions) != 0:
            for _ in enemy_minions:
                healths.append(_.get_health())
            max_val =max(healths)
            index_max =healths.index(max_val)
            return enemy_minions[index_max]
        else:
            return enemy_hero


class HearthModel():
    def __init__(self, player: Hero, active_player_minions: list[Minion], enemy: Hero, active_enemy_minions: list[Minion]):
        self._player = player
        self._active_player_minions =active_player_minions
        self._enemy = enemy
        self._active_enemy_minions =active_enemy_minions

    def __str__(self):
        # player minions
        player_minions_str = ";".join(
            f"{minion._symbol},{minion._health},{minion._shield}"
            for minion in self._active_player_minions
        )

        # enemy minions
        enemy_minions_str = ";".join(
            f"{minion._symbol},{minion._health},{minion._shield}"
            for minion in self._active_enemy_minions
        )

        return f"{self._player}|{player_minions_str}|{self._enemy}|{enemy_minions_str}"

    def __repr__(self):
        return (f"HearthModel({repr(self._player)}, {repr(self._active_player_minions)}, "
                f"{repr(self._enemy)}, {repr(self._active_enemy_minions)})")
    def get_player(self) -> Hero:
        return self._player

    def get_enemy(self) -> Hero:
        return self._enemy
    def get_player_minions(self) -> list[Minion]:
        return self._active_player_minions

    def get_enemy_minions(self) -> list[Minion]:
        return self._active_enemy_minions
    def has_won(self) -> bool:
        if self._player.is_alive() == True and self._enemy.is_alive()== False: # not sure how to get this to work need way of checking the enemy if player chosen and need way of checking the player if enemy chosen as self ?
            return True
        else:
            return False



    def has_lost(self) -> bool:
        return not self._player.is_alive()

    def play_card(self, card: Card, target: Entity) -> bool:
        pass

    def discard_card(self, card: Card):
        if card in self._player.get_hand():
            self._player.get_hand().remove(card)
            self._player.get_deck().add_card(card)





    def play_card(self, card: Card, target: Entity) -> bool:
        player = self._player

        # Check if player has enough energy and card is in hand
        if player.get_energy() < card.get_cost() or card not in player.get_hand():
            return False

    # Spend energy
        player.spend_energy(card.get_cost())

    # Remove card from hand
        player.get_hand().remove(card)

        if card.is_permanent():
        # Get health and shield from card's effect
            health = card.get_effect().get('health', 1)  # Default to 1 if not specified
            shield = card.get_effect().get('shield', 0)  # Default to 0 if not specified

        # Create minion using the card's class with the specified stats
            minion_class = card.__class__
            minion = minion_class(health=health, shield=shield)

        # Find first empty slot or add to end
            for i in range(len(self._active_player_minions)):
                if self._active_player_minions[i] is None:
                    self._active_player_minions[i] = minion
                    break
            else:
                self._active_player_minions.append(minion)

        # Clean up defeated minions
            self._active_player_minions = [m for m in self._active_player_minions if m is not None and m.is_alive()]
        else:
        # For non-permanent cards, apply effects to target
            if target is None:
                return False

            target.apply_effects(card.get_effect())

        # Clean up defeated minions if target was a minion
            if isinstance(target, Minion) and not target.is_alive():
                if target in self._active_player_minions:
                    self._active_player_minions.remove(target)
                elif target in self._active_enemy_minions:
                    self._active_enemy_minions.remove(target)

        return True

    def end_turn(self) -> list[str]:
        result = []

        # 1. Player's minions activate
        for minion in self._active_player_minions[:]:
            if minion and minion.is_alive():
                target = minion.choose_target(
                    ally_hero=self._player,
                    enemy_hero=self._enemy,
                    ally_minions=[m for m in self._active_player_minions if m != minion],
                    enemy_minions=self._active_enemy_minions
                )
                effect = minion.get_effect()
                if 'damage' in effect:
                    target.apply_damage(effect['damage'])
                if 'health' in effect:
                    target.apply_health(effect['health'])
                if 'shield' in effect:
                    target.apply_shield(effect['shield'])
                self._cleanup_defeated()

        # 2. Enemy turn processing
        if self._enemy.is_alive():
            # 2a. Enemy draws cards first
            while len(self._enemy.get_hand()) < 5 and not self._enemy.get_deck().is_empty():
                self._enemy.get_hand().extend(self._enemy.get_deck().draw_cards(1))

            # 2b. Increment Fireball turns
            for card in self._enemy.get_hand():
                if isinstance(card, Fireball):
                    card.increment_turn()

            # 2c. Simple left-to-right card playing
            played_cards = []
            remaining_energy = self._enemy.get_energy()

            for card in self._enemy.get_hand():  # Original order
                if remaining_energy >= card.get_cost():
                    # Get the card's full representation
                    card_repr = repr(card)

                    if card.is_permanent():
                        if len(self._active_enemy_minions) < 7:
                            minion = card.__class__(
                                health=card.get_effect().get('health', 1),
                                shield=card.get_effect().get('shield', 0)
                            )
                            for i in range(len(self._active_enemy_minions)):
                                if self._active_enemy_minions[i] is None:
                                    self._active_enemy_minions[i] = minion
                                    break
                            else:
                                self._active_enemy_minions.append(minion)
                            self._enemy.get_hand().remove(card)
                            played_cards.append(card_repr)
                            remaining_energy -= card.get_cost()




                    else:
                        # Simple targeting
                        if 'damage' in card.get_effect():
                            targets = [self._player] + self._active_player_minions
                        elif 'health' in card.get_effect() or 'shield' in card.get_effect():
                            targets = [self._enemy] + self._active_enemy_minions
                        else:
                            targets = []

                        if targets:
                            self.play_card(card, targets[0])
                            played_cards.append(card_repr)
                            remaining_energy -= card.get_cost()

            result.extend(played_cards)

            # 2d. Enemy minions activate
            for minion in self._active_enemy_minions[:]:
                if minion and minion.is_alive():
                    target = minion.choose_target(
                        ally_hero=self._enemy,
                        enemy_hero=self._player,
                        ally_minions=[m for m in self._active_enemy_minions if m != minion],
                        enemy_minions=self._active_player_minions
                    )
                    effect = minion.get_effect()
                    if 'damage' in effect:
                        target.apply_damage(effect['damage'])
                    if 'health' in effect:
                        target.apply_health(effect['health'])
                    if 'shield' in effect:
                        target.apply_shield(effect['shield'])
                    self._cleanup_defeated()

        return result

    def _cleanup_defeated(self):
        """Remove defeated minions and compact lists"""
        self._active_player_minions = [m for m in self._active_player_minions if m is not None and m.is_alive()]
        self._active_enemy_minions = [m for m in self._active_enemy_minions if m is not None and m.is_alive()]




def main() -> None:
    pass

if __name__ == "__main__":
    main()