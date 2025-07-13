#!/usr/bin/env python
# coding: utf-8

# - AIMA games4e.py 
# - AIMA utils4e.py
# - Time library

# In our project, we used the AIMA games4e.py to implement the AI player into the Mancala game. We also implemented the time library to measure how long it takes for the game simulation to complete. 

# - For the random vs. random players, we observed that out of 100 games, player 1 won about ~2% more than player 2. It's interesting to note that when we ran the test with 10,000 games, the difference was more noticeable--the first player won 48.29% of the time, while player 2 won 45.29%
# - From testing the minimax and alpha-beta players, the results were extraordinary--the first player won consistently above 90% of the games. In our test example at the bottom of this document, we observed that the AI player with minimax and alphabeta won ~93-98% with 5 plies.  

# Yes, there is ~2-3% advantage for the player with the first move. 

# - **Prompts player to enter a move:** we used the  `query_player(game, state)` function defined in games4e.py 
# - **Determines whether a move is legal or not:** `get_valid_moves(self, board, player)`
# - **Determines if someone has won and ends the game:** `terminal_test(self, state)` determines whether or not the game has ended, while `utility(self, state, player)` returns the score of the current board. If the score is positive --> the first player wins. If the score is negative --> the second player wins.

from games4e import *
import time 

def minmax_decision(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), depth + 1))
        return v

    def min_value(state, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), depth + 1))
        return v

    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a,), 1))

class Mancala(Game):
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones
        self.players = 2
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(board)-1-1]
        self.p2_mancala_index = len(board)-1

        # Zeroing the Mancala for both players
        board[self.p1_mancala_index] = 0
        board[self.p2_mancala_index] = 0

        self.starting_player = 1
        self.initial = GameState(to_move=self.starting_player,
                                 utility=0,
                                 board=board,
                                 moves=self.get_valid_moves(board, self.starting_player))

    def actions(self, state):
        return state.moves

    def get_valid_moves(self, board, player):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        # Determine the valid pit range for the current player.
        valid_pits_range = self.p1_pits_index if player == 1 else self.p2_pits_index
        valid_moves = []

        # Check if the pit has stones
        for pit in range(valid_pits_range[0], valid_pits_range[1] + 1):
            if board[pit] > 0:
                move = pit + 1 if player == 1 else pit - self.pits_per_player
                valid_moves.append(move)

        return valid_moves

    def display(self, state):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = state.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = state.board[self.p1_mancala_index]
        player_2_pits = state.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = state.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i],
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i],
                        player_2_pits[-(i+1)], self.pits_per_player - i))

        print('         {}         '.format(player_1_mancala))

    def get_pit_index(self, state, pit):
        """
        Function to convert player's pit to the pit index in the game board array

            P1      [7]       P2
                 ---------
        [0] 1 -> | 0 | 0 | <- 3 [6]
        [1] 2 -> | 0 | 0 | <- 2 [5]
        [2] 3 -> | 0 | 0 | <- 1 [4]
                 ---------
                    [3]
        """
        if state.to_move == 2:
            pit_index = pit + self.pits_per_player
        else:
            pit_index = pit - 1

        return pit_index

    def result(self, state, move):
        if move not in state.moves:
            print("INVALID MOVE\n")
            return state  # Illegal move has no effect

        state = copy.deepcopy(state)

        # Play the move
        self.play(state, move)

        # Update state
        next_player = state.to_move % self.players + 1
        next_player_moves = self.get_valid_moves(state.board, next_player)

        # print(f"{next_player}: {next_player_moves}")

        return GameState(to_move=next_player,
                         utility=None,
                         board=state.board,
                         moves=next_player_moves)

    def play(self, state, move):
        pit_index = self.get_pit_index(state, move)

        stones_to_distribute = state.board[pit_index]
        state.board[pit_index] = 0

        # Determine opponent's mancala index so we can skip over during the stone distribution
        opponent_mancala_index = self.p2_mancala_index if state.to_move == 1 else self.p1_mancala_index

        next_pit = (pit_index + 1) % len(state.board)
        last_pit = None

        # Distribute stones
        while stones_to_distribute > 0:
            if next_pit != opponent_mancala_index:
                state.board[next_pit] += 1
                stones_to_distribute -= 1
                last_pit = next_pit

            next_pit = (next_pit + 1) % len(state.board)

        # Check for capture: if the last stone landed in an empty pit on the current player's side.
        if last_pit is not None and state.board[last_pit] == 1:
            # Set player's pit range and mancala index.
            if state.to_move == 1:
                player_pits_range, player_mancala_index = self.p1_pits_index, self.p1_mancala_index
            else:
                player_pits_range, player_mancala_index = self.p2_pits_index, self.p2_mancala_index

            if player_pits_range[0] <= last_pit <= player_pits_range[1]:
                opposite_pit = self.pits_per_player * 2 - last_pit
                captured = state.board[last_pit] + state.board[opposite_pit]
                state.board[player_mancala_index] += captured
                state.board[last_pit] = 0
                state.board[opposite_pit] = 0

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        p1_stone_count = sum(state.board[self.p1_pits_index[0]:self.p1_pits_index[1] + 1])
        p2_stone_count = sum(state.board[self.p2_pits_index[0]:self.p2_pits_index[1] + 1])

        # Check if the game ends
        return p1_stone_count == 0 or p2_stone_count == 0

    def utility(self, state, player):
        # Sum the stones in the pits for each player
        p1_stone_count = sum(state.board[self.p1_pits_index[0]:self.p1_pits_index[1] + 1])
        p2_stone_count = sum(state.board[self.p2_pits_index[0]:self.p2_pits_index[1] + 1])

        # Check if the game ends
        if p1_stone_count == 0 or p2_stone_count == 0:

            p1_total_stones = p1_stone_count + state.board[self.p1_mancala_index]
            p2_total_stones = p2_stone_count + state.board[self.p2_mancala_index]

            # Update final board
            for i in range(len(state.board)):
                state.board[i] = 0
            state.board[self.p1_mancala_index] = p1_total_stones
            state.board[self.p2_mancala_index] = p2_total_stones

            final_score = p1_total_stones - p2_total_stones

            return final_score if player == 1 else -final_score

        immediate_score = state.board[self.p1_mancala_index] - state.board[self.p2_mancala_index] 

        return immediate_score if player == 1 else -immediate_score

    # Override AIMA method
    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        self.p1_move_count = 0
        self.p2_move_count = 0

        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)

                if state.to_move == 1:
                    self.p1_move_count += 1
                else:
                    self.p2_move_count += 1

                if self.terminal_test(state):
                    final_score = self.utility(state, self.to_move(self.initial))
                    self.display(state)
                    if final_score > 0:
                        print("Player 1 won!")
                    elif final_score < 0:
                        print("Player 2 won!")
                    else:
                        print("Tie!")
                    return final_score

alpha_beta_player_with_variable_plies = lambda plies: lambda game, state: alpha_beta_cutoff_search(state, game, plies)

minimax_player_with_variable_plies = lambda plies: lambda game, state: minmax_decision(state, game, plies)

mancala = Mancala(6, 4)


p1_win_count = 0
p2_win_count = 0
p1_total_moves = 0
p2_total_moves = 0
tie_count = 0
total_games = 100

# Start timing
start_time = time.perf_counter()

for i in range(total_games):
    final_score = mancala.play_game(random_player, random_player)
    if final_score > 0:
        p1_win_count += 1
        p1_total_moves += mancala.p1_move_count
    elif final_score < 0:
        p2_win_count += 1
        p2_total_moves += mancala.p2_move_count
    else:
        tie_count += 1

# End timing
end_time = time.perf_counter()

print()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")
print(f"Player 1 won {p1_win_count} games ({p1_win_count / total_games * 100:.2f}%).")
if p1_win_count > 0:
    print(f"Player 1 average move to win the game is {p1_total_moves / p1_win_count:.2f}.")
print(f"Player 2 won {p2_win_count} games ({p2_win_count / total_games * 100:.2f}%).")
if p2_win_count > 0:
    print(f"Player 2 average move to win the game is {p2_total_moves / p2_win_count:.2f}.")
print(f"Tie count: {tie_count} times ({tie_count / total_games * 100:.2f}%).")

# We customized the original minimax function from games4e.py to handle the variable of plies (we use 1 plies for testing). The logic is placed in the `minmax_decision(state, game, d=4, cutoff_test=None, eval_fn=None)` function to cater more to our custom game needs such as the cutoff. The player function is defined in `minimax_player_with_variable_plies(1)`


p1_win_count = 0
p2_win_count = 0
p1_total_moves = 0
p2_total_moves = 0
tie_count = 0
total_games = 100

# Start timing
start_time = time.perf_counter()

for i in range(total_games):
    final_score = mancala.play_game(minimax_player_with_variable_plies(4), random_player)
    if final_score > 0:
        p1_win_count += 1
        p1_total_moves += mancala.p1_move_count
    elif final_score < 0:
        p2_win_count += 1
        p2_total_moves += mancala.p2_move_count
    else:
        tie_count += 1

# End timing
end_time = time.perf_counter()

print()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")
print(f"Player 1 won {p1_win_count} games ({p1_win_count / total_games * 100:.2f}%).")
if p1_win_count > 0:
    print(f"Player 1 average move to win the game is {p1_total_moves / p1_win_count:.2f}.")
print(f"Player 2 won {p2_win_count} games ({p2_win_count / total_games * 100:.2f}%).")
if p2_win_count > 0:
    print(f"Player 2 average move to win the game is {p2_total_moves / p2_win_count:.2f}.")
print(f"Tie count: {tie_count} times ({tie_count / total_games * 100:.2f}%).")


p1_win_count = 0
p2_win_count = 0
p1_total_moves = 0
p2_total_moves = 0
tie_count = 0
total_games = 100

# Start timing
start_time = time.perf_counter()

for i in range(total_games):
    final_score = mancala.play_game(minimax_player_with_variable_plies(5), random_player)
    if final_score > 0:
        p1_win_count += 1
        p1_total_moves += mancala.p1_move_count
    elif final_score < 0:
        p2_win_count += 1
        p2_total_moves += mancala.p2_move_count
    else:
        tie_count += 1

# End timing
end_time = time.perf_counter()

print()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")
print(f"Player 1 won {p1_win_count} games ({p1_win_count / total_games * 100:.2f}%).")
if p1_win_count > 0:
    print(f"Player 1 average move to win the game is {p1_total_moves / p1_win_count:.2f}.")
print(f"Player 2 won {p2_win_count} games ({p2_win_count / total_games * 100:.2f}%).")
if p2_win_count > 0:
    print(f"Player 2 average move to win the game is {p2_total_moves / p2_win_count:.2f}.")
print(f"Tie count: {tie_count} times ({tie_count / total_games * 100:.2f}%).")


p1_win_count = 0
p2_win_count = 0
p1_total_moves = 0
p2_total_moves = 0
tie_count = 0
total_games = 100

# Start timing
start_time = time.perf_counter()

for i in range(total_games):
    final_score = mancala.play_game(alpha_beta_player_with_variable_plies(5), random_player)
    if final_score > 0:
        p1_win_count += 1
        p1_total_moves += mancala.p1_move_count
    elif final_score < 0:
        p2_win_count += 1
        p2_total_moves += mancala.p2_move_count
    else:
        tie_count += 1

# End timing
end_time = time.perf_counter()

print()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")
print(f"Player 1 won {p1_win_count} games ({p1_win_count / total_games * 100:.2f}%).")
if p1_win_count > 0:
    print(f"Player 1 average move to win the game is {p1_total_moves / p1_win_count:.2f}.")
print(f"Player 2 won {p2_win_count} games ({p2_win_count / total_games * 100:.2f}%).")
if p2_win_count > 0:
    print(f"Player 2 average move to win the game is {p2_total_moves / p2_win_count:.2f}.")
print(f"Tie count: {tie_count} times ({tie_count / total_games * 100:.2f}%).")


p1_win_count = 0
p2_win_count = 0
p1_total_moves = 0
p2_total_moves = 0
tie_count = 0
total_games = 100

# Start timing
start_time = time.perf_counter()

for i in range(total_games):
    final_score = mancala.play_game(alpha_beta_player_with_variable_plies(10), random_player)
    if final_score > 0:
        p1_win_count += 1
        p1_total_moves += mancala.p1_move_count
    elif final_score < 0:
        p2_win_count += 1
        p2_total_moves += mancala.p2_move_count
    else:
        tie_count += 1

# End timing
end_time = time.perf_counter()

print()
print(f"Elapsed time: {end_time - start_time:.4f} seconds")
print(f"Player 1 won {p1_win_count} games ({p1_win_count / total_games * 100:.2f}%).")
if p1_win_count > 0:
    print(f"Player 1 average move to win the game is {p1_total_moves / p1_win_count:.2f}.")
print(f"Player 2 won {p2_win_count} games ({p2_win_count / total_games * 100:.2f}%).")
if p2_win_count > 0:
    print(f"Player 2 average move to win the game is {p2_total_moves / p2_win_count:.2f}.")
print(f"Tie count: {tie_count} times ({tie_count / total_games * 100:.2f}%).")

# In[ ]:

mancala.play_game(alpha_beta_player_with_variable_plies(5), query_player)

# In[ ]:

