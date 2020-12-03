from game import Game
from agent import HumanAgent
from mctc_agent import AIAgent
from random_agent import RandomAgent

import numpy as np


if __name__ == "__main__":
    mctc_random_game = Game()

    ai_1 = AIAgent(mctc_random_game, save_tree_after_game=True)
    random_agent = RandomAgent(mctc_random_game)

    for i in range(5000):
        print(i)
        agents = [ai_1, AIAgent(mctc_random_game), random_agent]
        agent_1, agent_2 = np.random.choice(agents, 2, replace=False)
        while ai_1 is not agent_1 and ai_1 is not agent_2:
            print('reselect players while non of these would change the saved tree')
            agent_1, agent_2 = np.random.choice(agents, 2, replace=False)
        print('players: ', agent_1, agent_2)
        mctc_random_game.play_a_game(agent_1, agent_2)

    mctc_random_game.play_a_game(HumanAgent(mctc_random_game), ai_1)
