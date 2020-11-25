import numpy as np

from agent import Agent
from game import Game
from random_agent import RandomAgent

from utils import get_possible_steps, execute_step



class StateInfNode():
    def __init__(self, game_state: np.array):
        super(StateInfNode, self).__init__()

        self.state = game_state

        self.visited = 0
        self.won_from_here = 0

    @staticmethod
    def get_key(game_state: np.array):
        return game_state.tobytes()

    def get_state(self):
        return self.state

    def valid_steps(self):
        return get_possible_steps(self.state)

    def get_child_state_by_idx(self, step_idx: int):
        step = get_possible_steps(self.state)[step_idx]
        return execute_step(self.state, step)

    def get_child_state_by_step(self, step: int):
        assert step in get_possible_steps(self.state)
        return execute_step(self.state, step)

class AIAgent(Agent):
    def __init__(self, game: Game):
        super(AIAgent, self).__init__(game)
        self.helper_agent = RandomAgent(game)

        self.step_hist = []
        self.last_known_state_key = None
        self.state_search_tree = {}

    def game_started(self, initial_state: np.array):
        init_state_key = StateInfNode.get_key(initial_state)
        if self.state_search_tree == {}:
            self.state_search_tree[init_state_key] = StateInfNode(initial_state)
        self.last_known_state_key = init_state_key

    def step(self, game_state: np.array, last_step: int):
        self._update_tree_with_last_step(game_state, last_step)
        self.make_children_available()

        step_to_take = self.select(game_state, last_step)

        new_state = self.state_search_tree[self.last_known_state_key].get_child_state_by_step(step_to_take)
        self.last_known_state_key = StateInfNode.get_key(new_state)
        self.step_hist.append(step_to_take)

        print(step_to_take)
        for key in self.state_search_tree:
            print('\t', self.state_search_tree[key].get_state())
        print(self.step_hist)

        return step_to_take


    def game_ended(self, has_won: bool):
        pass

    def select(self, game_state: np.array, last_step: int):
        return self.helper_agent.step(game_state, last_step)

    def _update_tree_with_last_step(self, game_state: np.array, last_step: int):
        new_state = self.state_search_tree[self.last_known_state_key].get_child_state_by_step(last_step)
        # assert (new_state == game_state).all()

        new_state_key = StateInfNode.get_key(new_state)
        if new_state_key not in self.state_search_tree.keys():
            self.state_search_tree[new_state_key] = StateInfNode(new_state)
        self.last_known_state_key = new_state_key

        self.step_hist.append(last_step)

    def make_children_available(self):
        curr_state_inf_node = self.state_search_tree[self.last_known_state_key]
        for valid_step in curr_state_inf_node.valid_steps():
            child_state = curr_state_inf_node.get_child_state_by_step(valid_step)
            child_step_key = StateInfNode.get_key(child_state)
            if child_step_key not in self.state_search_tree.keys():
                self.state_search_tree[child_step_key] = StateInfNode(child_state)





