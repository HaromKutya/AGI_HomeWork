from game import Game
from agent import HumanAgent
from mctc_agent import AIAgent


if __name__ == "__main__":
    human_agent = HumanAgent()
    random_agent = AIAgent()

    human_random_game = Game(human_agent, random_agent)

    human_random_game.play_a_game()
