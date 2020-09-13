"""main script"""
from Player import Player, evolve_player
from Game import Game

import numpy as np
import pandas as pd
from multiprocessing import Pool
import time

#Parameters for running the program
ngames   = 100
nplayers = 100
nepochs  = 5000

# Generating the players
players = [Player() for i in range(nplayers)]

# Tracking dataframe
df = pd.DataFrame(columns = ['players'])
for player in players:
	df.loc[player.idno] = player

for epoch in range(nepochs):
	epoch_start = time.time()
	# Assigning players randomly to different games
	print('Assigning Players')
	players = df.players.values.copy()
	gameplayers = [np.random.choice(players, size = 4, replace=False) for i in range(ngames)]
	print('Running games')

	# Running the games
	t0 = time.time()
	for i in range(ngames):
		game = Game(players = gameplayers[i])
		game.run_game()
	print(f'Running {ngames} games in {time.time() - t0:.2f}s')

	
	game.plot_card_play(savefig = True, savefig_name = f'../images/epoch_{epoch}_game_{i}_cardplay.pdf')
	game.plot_bidding(savefig = True, savefig_name = f'../images/epoch_{epoch}_game_{i}_bidding.pdf')

	print('Generating new Players')
	# Adding scores to dataframe
	df['score'] = 0
	for player in players:
		df.loc[player.idno,'score'] = player.score
	df = df.sort_values('score', ascending=False)

	# Selecting only players with positive scores
	df = df.loc[df.score > max(0, df.score.mean())]

	# Evolving new players based on the ones which did well.
	n_new = nplayers - len(df)
	players = df.players.values
	pvec = df.score / df.score.sum()

	for i in range(n_new):
		parent = np.random.choice(players, p = pvec)
		newplayer = evolve_player(parent, probabilities=[0.1]*6 )
		df.loc[newplayer.idno] = [newplayer, 0]
	print(f'Finished epoch {epoch} / {nepochs} in {time.time() - epoch_start:.2f}s')