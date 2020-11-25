from game import Game
from agent import HumanAgent
from mctc_agent import AIAgent
from random_agent import RandomAgent


if __name__ == "__main__":
    human_random_game = Game()

    human_agent = HumanAgent(human_random_game)
    random_agent = AIAgent(human_random_game)

    human_random_game.play_a_game(human_agent, random_agent)
