import numpy as np
import json
import os

from agent import Agent
from game import Game
from random_agent import RandomAgent

from utils import get_possible_steps, execute_step, has_game_ended


class StateInfNode():
    def __init__(self, game_state: np.array):
        super(StateInfNode, self).__init__()

        self.state = game_state

        self.visited = 0
        self.won_from_here = 0

    @staticmethod
    def encode_state(game_state: np.array):
        compList = []
        for row in game_state:
            compList.append(''.join(map(str, row.flatten())))
        return ';'.join(compList)

    @staticmethod
    def decode_state(game_state_label: str):
        game_state_list = []
        for row in game_state_label.split(';'):
            game_state_list.append(list(row))
        state = np.asarray(game_state_list, dtype=int)
        return state



    def get_state(self):
        return self.state

    def valid_steps(self):
        return get_possible_steps(self.state)

    def get_child_state_by_idx(self, step_idx: int):
        step = get_possible_steps(self.state)[step_idx]
        return execute_step(self.state, step)

    def get_child_state_by_step(self, step: int):
        if step not in get_possible_steps(self.state):
            print(self.state)
            print(step)
        assert step in get_possible_steps(self.state)
        return execute_step(self.state, step)

    def visit_step(self, has_won):
        self.visited += 1
        if has_won:
            self.won_from_here += 1


class AIAgent(Agent):
    def __init__(self, game: Game, helper_agent: Agent = RandomAgent, save_tree_after_game=False,
                 state_search_tree=None):
        super(AIAgent, self).__init__(game)
        self.helper_agent = helper_agent(game)
        self.save_tree_after_game = save_tree_after_game

        self.step_hist = []
        self.last_known_state_key = None
        if state_search_tree is None:
            self.state_search_tree = {}
        else:
            self.state_search_tree = state_search_tree
        self.initial_state_key = None

    def game_started(self, initial_state: np.array):
        init_state_key = StateInfNode.encode_state(initial_state)
        if self.state_search_tree == {}:
            self.load_search_tree()
        if self.state_search_tree == {}:
            self.state_search_tree[init_state_key] = StateInfNode(initial_state)
        self.last_known_state_key = init_state_key
        self.initial_state_key = init_state_key

    def step(self, game_state: np.array, last_step: int):
        if last_step >= 0:
            self._update_tree_with_last_step(game_state, last_step)
        self.expand_when_needed()

        step_to_take = self.select(game_state, last_step)

        new_state = self.state_search_tree[self.last_known_state_key].get_child_state_by_step(step_to_take)
        self.last_known_state_key = StateInfNode.encode_state(new_state)
        self.step_hist.append(step_to_take)

        # print(step_to_take)

        return step_to_take

    def game_ended(self, has_won: bool, last_game_state: np.array, last_step: int):
        if not has_won and last_step in self.state_search_tree[self.last_known_state_key].valid_steps():
            self._update_tree_with_last_step(last_game_state, last_step)
        # print()
        print('has_won:', has_won)
        print('init state visited:', self.state_search_tree[self.initial_state_key].visited)
        print('number of nodes in search tree:', len(self.state_search_tree.keys()))
        # print(self.step_hist)
        self.back_propagate(has_won)

        if self.save_tree_after_game:
            self.save_search_tree()
        # print('tree length:', len(self.state_search_tree.keys()))
        # for i, key in enumerate(self.state_search_tree):
        #     # print('\t', self.state_search_tree[key].get_state())
        #     print(f'\t{self.state_search_tree[key].won_from_here}/{self.state_search_tree[key].visited}')
        #     if i > 10:
        #         break

        # print()
        self.step_hist = []
        self.last_known_state_key = None

    def select(self, game_state: np.array, last_step: int):
        curr_state_node = self.state_search_tree[self.last_known_state_key]
        valid_steps = get_possible_steps(curr_state_node.state)
        valid_step_probs = []

        child_wins = np.zeros(len(valid_steps))
        child_visits = np.zeros(len(valid_steps))
        for i, step in enumerate(valid_steps):
            child_wins[i], child_visits[i] = self.child_won_visited_simulate_if_needed(step)

        step_idx = self.step_idx_to_take_UCB(child_wins, child_visits)

        return valid_steps[step_idx]

    def child_won_visited_simulate_if_needed(self, step: int):
        curr_state_node = self.state_search_tree[self.last_known_state_key]
        child_state = curr_state_node.get_child_state_by_step(step)
        child_state_key = StateInfNode.encode_state(child_state)
        child_state_node = self.state_search_tree[child_state_key]

        visits = child_state_node.visited
        if visits < 1:
            self.simulate_random_game_with_first_step_provided(step)
            visits = child_state_node.visited
        wins = child_state_node.won_from_here
            
        return wins, visits

    def simulate_random_game_with_first_step_provided(self, first_step: int):
        curr_state_node = self.state_search_tree[self.last_known_state_key]
        board_state = curr_state_node.get_child_state_by_step(first_step)

        winner = has_game_ended(board=board_state, last_step=first_step)
        step_to_take = first_step
        while winner == 0:
            step_to_take = self.helper_agent.step(board_state, step_to_take)
            board_state = execute_step(board_state, step_to_take)
            winner = has_game_ended(board=board_state, last_step=step_to_take)

        alt_history = self.step_hist + [first_step]
        if winner == 1:
            self.back_propagate_step_history(alt_history, has_won=True)
        else:
            self.back_propagate_step_history(alt_history, has_won=False)

    def step_idx_to_take_softmax(self, child_wins, child_visits, eps=.0001):
        valid_step_probs = (child_wins+eps) / (child_visits+eps)
        valid_step_probs = np.exp(valid_step_probs) / np.sum(np.exp(valid_step_probs))
        step_idx = np.random.choice(len(child_wins), 1, replace=False, p=valid_step_probs)
        return step_idx

    def step_idx_to_take_UCB(self, child_wins, child_visits, exploration_rate=1):
        child_wins, child_visits = child_wins, child_visits
        exploitation_component = child_wins / child_visits
        ln_sum_visits = np.log(np.sum(child_visits))
        exploration_component = exploration_rate * np.sqrt(ln_sum_visits/child_visits)
        fitness = exploitation_component + exploration_component + .00001 * np.random.random(exploitation_component.shape)
        return np.argmax(fitness)

    def expand_when_needed(self):
        curr_state_inf_node = self.state_search_tree[self.last_known_state_key]
        for valid_step in curr_state_inf_node.valid_steps():
            child_state = curr_state_inf_node.get_child_state_by_step(valid_step)
            child_step_key = StateInfNode.encode_state(child_state)
            if child_step_key not in self.state_search_tree.keys():
                self.state_search_tree[child_step_key] = StateInfNode(child_state)

    def _update_tree_with_last_step(self, game_state: np.array, last_step: int):
        new_state = self.state_search_tree[self.last_known_state_key].get_child_state_by_step(last_step)
        # assert (new_state == game_state).all()

        new_state_key = StateInfNode.encode_state(new_state)
        if new_state_key not in self.state_search_tree.keys():
            self.state_search_tree[new_state_key] = StateInfNode(new_state)
        self.last_known_state_key = new_state_key

        self.step_hist.append(last_step)

    def back_propagate(self, has_won: bool):
        self.back_propagate_step_history(self.step_hist, has_won)

    def back_propagate_step_history(self, step_hist: list, has_won: bool):
        state_key = self.initial_state_key
        state_inf_node = self.state_search_tree[state_key]
        state_inf_node.visit_step(has_won)
        for step in step_hist:
            assert step in state_inf_node.valid_steps()
            child_state = state_inf_node.get_child_state_by_step(step)
            state_key = StateInfNode.encode_state(child_state)
            state_inf_node = self.state_search_tree[state_key]
            state_inf_node.visit_step(has_won)

    def save_search_tree(self):
        tree_list = [
            [StateInfNode.encode_state(node.state), node.won_from_here, node.visited]
            for key, node in self.state_search_tree.items()
        ]
        with open('search_tree.json', 'w') as f:
            json.dump(tree_list, f)

    def load_search_tree(self):
        save_dict = {}
        if os.path.isfile('search_tree.json'):
            with open('search_tree.json', 'r') as f:
                tree_list = json.load(f)
            for [state_key, won_from_here, visited] in tree_list:
                state = StateInfNode.decode_state(state_key)
                new_node = StateInfNode(state)
                new_node.won_from_here = won_from_here
                new_node.visited = visited
                save_dict[state_key] = new_node

        self.state_search_tree = save_dict
