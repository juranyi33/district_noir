import random


class DistrictNoir:
    def __init__(self, deck, line, round):
        self.deck = deck
        self.line = line
        self.round = round
        self.num_of_rounds = 4

    def setup_game(self):
        for _ in range(3):
            self.deck.draw_card()  # Remove three cards for game setup

        self.line = [self.deck.draw_card() for _ in range(2)]  # draw 2 cards to begin the line

    def get_opponent(self, player, players):
        for possible_player in players:
            if possible_player.id == player.id * -1:
                new_player = possible_player
                return new_player

    def has_city_card_victory(self, players):
        for player in players:
            if sum(1 for card in player.stash if card.is_city_card()) == 3:
                return True, player
        return False, None

    def is_all_rounds_completed(self):
        return self.round >= self.num_of_rounds


class Card:
    def __init__(self, card_type, value=None, points=None):
        self.card_type = card_type  # 'support', 'direct-point', 'city'
        self.value = value  # For support cards
        self.points = points  # For direct-point cards
        # Use None for attributes that do not apply to a specific card type

    def is_city_card(self):
        return self.card_type == 'city'

    def is_support_card(self):
        return self.card_type == 'support'

    def is_direct_point_card(self):
        return self.card_type == 'direct-point'

    def display(self):
        if self.is_city_card():
            return "[City Card]"
        elif self.is_support_card():
            return f"[Sup: Value {self.value}]"
        elif self.is_direct_point_card():
            return f"[DP: {self.points} points]"
        else:
            return "[Unknown Card]"


class Deck:
    def __init__(self, cards=None):
        self.cards = cards if cards is not None else []
        self.initialize_deck()

    def initialize_deck(self):
        # Add Support Cards
        for value in range(5, 9):  # Values 5 to 8
            for _ in range(value):
                self.cards.append(Card(card_type='support', value=value))

        # Add Direct-Point Cards
        dp_card_values = {-3: 3, -2: 4, -1: 2, 2: 4, 3: 2, 4: 1}  # Points: Quantity
        for points, quantity in dp_card_values.items():
            for _ in range(quantity):
                self.cards.append(Card(card_type='direct-point', points=points))

        # Add City Cards
        for _ in range(3):
            self.cards.append(Card(card_type='city'))

        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)  # Draw the top card from the deck
        return None  # Return None if the deck is empty


class Player:
    def __init__(self, id, points=0):
        self.id = id
        self.hand = []
        self.stash = []
        self.actions_left = 6
        self.already_collected = False
        self.points = points

    def display_cards(self):
        if len(self.hand) > 0:
            print(f"player{self.id}'s hand: ")
            for card in self.hand:
                print(card.display())
        else:
            print(f"player{self.id}'s hand is empty")
        if len(self.stash) > 0:
            print(f"player{self.id}'s stash: ")
            for card in self.stash:
                print(card.display())
        else:
            print(f"player{self.id}'s stash is empty")

    def draw_round_start(self, deck):
        self.hand = [deck.draw_card() for _ in range(5)]

    def collect(self, line):
        self.already_collected = True
        # Determine the number of cards to collect
        num_cards_to_collect = min(5, len(line))

        # Collect the last 'num_cards_to_collect' cards from the line
        collected_cards = line[-num_cards_to_collect:]
        self.stash.extend(collected_cards)

        # Remove the collected cards from the line
        del line[-num_cards_to_collect:]

        # Print information about the collection
        print(f"Player {self.id} collected the following cards:")
        for card in collected_cards:
            print(card.display())
        print("\n")
        print("Current Line:")
        for card_in_line in line:
            print(card_in_line.display())

    def place_card(self, card, line):
        # Add the chosen card to the end of the line
        line.append(card)
        print("Current Line:")
        for card_in_line in line:
            print(card_in_line.display())

    def get_player_action(self, district_noir):
        self.actions_left -= 1
        while True:
            if (len(self.hand) == 0) & (not self.already_collected):
                print("Had no choice, but to collect")
                self.collect(district_noir.line)  # For a reason, the cards went to both players stashes
                break
            else:
                action = input(f"Player {self.id} to choose an action:")
                if action == "place":
                    # Implement logic to choose which card to place
                    for index, card in enumerate(self.hand):
                        print(f"{index}: {card.display()}")

                    # Get the player's choice
                    card_index = input(f"Player {self.id}, select a card to place by index: ")
                    try:
                        card_index = int(card_index)
                        if 0 <= card_index < len(self.hand):
                            card_to_place = self.hand.pop(card_index)
                            self.place_card(card_to_place, district_noir.line)
                            break
                        else:
                            print("Invalid index. Please try again.")
                            continue
                    except ValueError:
                        print("Please enter a valid number.")
                        continue
                    self.place_card(card_to_place, district_noir.line)
                    break
                elif action == "collect":
                    if self.already_collected:
                        print(f"Player {self.id} has already collected in this round")
                    else:
                        if len(district_noir.line)==0:
                            print(f"The line has no cards, you have to place")
                        else:
                            self.collect(district_noir.line)
                            break
                else:
                    print("Invalid action. Please choose 'place' or 'collect'.")
                    continue

    def calculate_support_card_score(self, opponent):
        score = 0
        for value in range(5, 9):
            player_count = sum(1 for card in self.stash if card.is_support_card() and card.value == value)
            opponent_count = sum(1 for card in opponent.stash if card.is_support_card() and card.value == value)
            if player_count > opponent_count:
                score += value
        return score

    def calculate_dp_card_score(self):
        return sum(card.points for card in self.stash if card.is_direct_point_card())

    def calculate_set_bonus(self):
        # Counts the number of each support card value in the player's stash
        value_counts = {value: 0 for value in range(5, 9)}
        for card in self.stash:
            if card.is_support_card():
                value_counts[card.value] += 1

        # The number of complete sets is the minimum count among the four values
        complete_sets = min(value_counts.values())

        # Each complete set is worth 5 points
        return complete_sets * 5

    def calculate_total_score(self, opponent):
        support_score = self.calculate_support_card_score(opponent)
        dp_score = self.calculate_dp_card_score()
        # Assuming the implementation of a method to check complete sets
        set_bonus = self.calculate_set_bonus()
        self.points = support_score + dp_score + set_bonus
