from poker_game_runner.state import Observation, PlayerInfo
from poker_game_runner.utils import Range, HandType
import time
import random

BOT_NAME = "Lisbeth Marianne Christensen" # Change this to your bot's name

class Bot:
  @classmethod
  def get_name_class(cls, path):
    return BOT_NAME

  def get_name(self):
    return BOT_NAME

  def passive(self, obs: Observation):
    my_hand = obs.get_my_hand_type()
    board = obs.get_board_hand_type()

    if obs.get_call_size() > obs.get_my_player_info().stack * 0.1:
      return 0
    elif my_hand > board:
      return obs.get_min_raise()
    else:
      return 1

  def aggressive(self, obs: Observation):
    my_hand = obs.get_my_hand_type()

    raise_hand = Range("22+", "A2s+", "K2s+", "Q5s+", "J7s+", "T7s+", "98s", "A6o+", "K7o+", "Q8o+", "J9o+", "T9o")

    if raise_hand.is_hand_in_range(my_hand):
      return obs.get_min_raise() * 0.05
    else:
      return 0

  def positive(self, obs: Observation):
    random_int = random.randint(0, 3)

    decent_hand = Range("77+, A8s+, K9s+, QTs+, AJo+, KQo")

    if (random_int == 0):
      # Will 'call' if bot has a decent hand else it will 'fold'
      if (decent_hand.is_hand_in_range(obs.my_hand)):
        return 1
      return 0

    elif (random_int == 1):
      # Will go 'all in' if the round is 4 else it will 'call'
      if (obs.current_round == 4):
        return obs.get_max_raise()
      return 1

    else:
      # If handtype is a straightflush then all in
      if obs.get_my_hand_type() == HandType.STRAIGHTFLUSH:
        return obs.get_max_raise()
      # Are we feeling lucky?
      # If yes then 'all in' else 'call'
      return obs.get_max_raise() if random.randint(0, 1000) == 1000 else 1

  def act(self, obs: Observation):
    # Initial strategy weights
    if self.strategies is None:
      self.strategies = [1., 0.5, 0.75]

    strategy = random.range(0., sum(self.strategies))

    if self.strategy is None:
      if strategy < self.strategies[0]:
        self.strategy = 0
      elif strategy < sum(self.strategies[0:2]):
        self.strategy = 1
      else:
        self.strategy = 2
      self.last_strategy = strategy

    # Choose act
    act = 0
    if self.strategy == 0:
      act = self.passive()
    elif self.strategy == 1:
      act = self.aggressive()
    elif self.strategy == 2:
      act = self.positive()

    if len(obs.board_cards) == 5:
      self.last_stack = obs.get_my_player_info().stack
      self.last_strategy = self.strategy
      self.strategy = None
    elif len(obs.board_cards) == 0 and self.last_stack is not None:
      # Update strategy 
      if obs.get_my_player_info().stack > self.last_stack:
        self.strategies[self.last_strategy] *= 1.05
      else:
        self.strategies[self.last_strategy] *= 0.97
      self.last_stack = obs.get_my_player_info().stack
    
    return act
