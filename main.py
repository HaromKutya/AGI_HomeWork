from game import Game
from agent import HumanAgent
from mctc_agent import AIAgent
from random_agent import RandomAgent, CentroidRandomAgent, GreedyRandomAgent, MinimalistRandomAgent

import time
import numpy as np


if __name__ == "__main__":
    burn_in = 0

    mctc_random_game = Game()

    ai_1 = AIAgent(mctc_random_game)

    random_agents = [RandomAgent(mctc_random_game),
                     CentroidRandomAgent(mctc_random_game),
                     GreedyRandomAgent(mctc_random_game),
                     MinimalistRandomAgent(mctc_random_game)]

    log_file = open("training_log_" + str(int(time.time())) + ".csv", 'w')
    log_file.write("iteration,burn_in,opponent,starting_player,winner,ai_node_count,root_visited,step_count\n")

    for i in range(20000):
        print('Iteration ' + str(i))
        if i > burn_in and np.random.random() < 0.7:
            opponent_index = 0
            opponent = AIAgent(mctc_random_game)
        else:
            opponent_index = np.random.choice(len(random_agents), 1)[0]
            opponent = random_agents[opponent_index]
            opponent_index += 1
        # opponent_index = -1
        # opponent = HumanAgent(mctc_random_game)
        agent_1, agent_2 = np.random.choice([ai_1, opponent], 2, replace=False)
        # while ai_1 is not agent_1 and ai_1 is not agent_2:
        #     print('reselect players because non of these would change the saved tree')
        #     agent_1, agent_2 = np.random.choice(agents, 2, replace=False)
        print('players: ', agent_1, agent_2)
        winner = mctc_random_game.play_a_game(agent_1, agent_2)

        node_count = len(ai_1.state_search_tree)
        root_visited = ai_1.state_search_tree[ai_1.initial_state_key].visited
        step_count = np.sum(mctc_random_game.board != 0)
        log_file.write(','.join([str(i),
                                 str(int(i <= burn_in)),
                                 str(opponent_index),
                                 str(1 if agent_1 is ai_1 else 2),
                                 str(winner),
                                 str(node_count),
                                 str(root_visited),
                                 str(step_count)]) + '\n')

        if (i + 1) % 20 == 0:
            ai_1.save_search_tree()

    log_file.close()
    # mctc_random_game.play_a_game(HumanAgent(mctc_random_game), ai_1)
