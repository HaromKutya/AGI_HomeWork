from game import Game
from agent import HumanAgent
from mctc_agent import AIAgent
from random_agent import RandomAgent

import numpy as np


if __name__ == "__main__":
    mctc_random_game = Game()

    ai_1 = AIAgent(mctc_random_game)
    ai_2 = AIAgent(mctc_random_game)
    random_agent = RandomAgent(mctc_random_game)
    agents = [ai_1, ai_2, random_agent]

    for i in range(1000):
        print(i)
        agent_1, agent_2 = np.random.choice(agents, 2, replace=False)
        print('players: ', agent_1, agent_2)
        mctc_random_game.play_a_game(agent_1, agent_2)

    mctc_random_game.play_a_game(ai_1, RandomAgent(mctc_random_game))
    print(mctc_random_game.board)
    mctc_random_game.play_a_game(RandomAgent(mctc_random_game), ai_1)
    print(mctc_random_game.board)
    mctc_random_game.play_a_game(ai_2, RandomAgent(mctc_random_game))
    print(mctc_random_game.board)
    mctc_random_game.play_a_game(RandomAgent(mctc_random_game), ai_2)
    print(mctc_random_game.board)

    while(True):
        mctc_random_game.play_a_game(HumanAgent(mctc_random_game), ai_1)
