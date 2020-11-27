from game import Game
from agent import HumanAgent
from mctc_agent import AIAgent
from random_agent import RandomAgent


if __name__ == "__main__":
    human_random_game = Game()

    ai_1 = AIAgent(human_random_game)
    ai_2 = AIAgent(human_random_game)

    for i in range(5000):
        print(i)
        if i % 2 == 0:
            human_random_game.play_a_game(ai_1, ai_2)
        else:
            human_random_game.play_a_game(ai_2, ai_1)

    human_random_game.play_a_game(ai_1, RandomAgent(human_random_game))
    print(human_random_game.board)
    human_random_game.play_a_game(RandomAgent(human_random_game), ai_1)
    print(human_random_game.board)
    human_random_game.play_a_game(ai_2, RandomAgent(human_random_game))
    print(human_random_game.board)
    human_random_game.play_a_game(RandomAgent(human_random_game), ai_2)
    print(human_random_game.board)

    while(True):
        human_random_game.play_a_game(HumanAgent(human_random_game), ai_1)
