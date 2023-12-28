from district_noir import Deck, Player, DistrictNoir

player1 = Player(id=1)
player2 = Player(id=-1)
players = [player1, player2]
deck = Deck()

district_noir = DistrictNoir(deck=deck, line=[], round=0)
district_noir.setup_game()

while True:
    for round_number in range(1, district_noir.num_of_rounds + 1):
        print(f"Round {round_number} starts.")

        # Ensure hands are empty and draw new hands at round start
        for player in players:
            if len(player.hand) > 0:  # Error could be initialized
                print(f"Warning: Player {player.id}'s hand should be empty. Resetting hand.")
                player.hand = []
            player.draw_round_start(deck)
            # Reset actions for each player at the start of the round
            player.actions_left = 6

        # Time for actions!
        while any(player.actions_left > 0 for player in players):
            for player in players:
                if player.actions_left > 0:
                    # Implement logic for player to choose and perform an action
                    # For example, player.place_card() or player.collect()
                    # Decrease the action count after each action
                    player.get_player_action(district_noir)  # either be a collect or a placing"
                    city_card_victory, city_win_player = district_noir.has_city_card_victory(players)
                    # Check for immediate game-over condition (3 city cards)
                    if city_card_victory:
                        print(f"Game over!Player {city_win_player.id} wins with 3 city cards!")
                        break
            if city_card_victory:
                break
        print(f"Round {round_number} ends.")

        district_noir.round += 1
        # Check for immediate game-over condition (3 city cards)
        # Maybe this could be inside a round and not out-side. Why
        # would the players make all their 6 actions if
        city_card_victory, city_win_player = district_noir.has_city_card_victory(players)
        if city_card_victory:
            print(f"Game over! {city_win_player.name} wins with 3 city cards!")
            break

    if district_noir.is_all_rounds_completed():
        # Calculate scores for each player
        player1.calculate_total_score(player2)
        player2.calculate_total_score(player1)

        # Display final scores
        print(f"Player 1 Score: {player1.points}, Player 2 Score: {player2.points}")

        # Determine the winner
        if player1.points > player2.points:
            print("Player 1 wins!")
        elif player2.points > player1.points:
            print("Player 2 wins!")
        else:
            print("It's a tie!")

        break
