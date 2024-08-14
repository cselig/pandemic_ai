import abc
import random

import simplified_pandemic.data_structures as ds


class Policy(abc.ABC):

  @abc.abstractmethod
  def get_move(self, state: ds.BoardState) -> ds.Move:
    raise NotImplementedError()


class RandomPolicy(Policy):
  """Makes a random move."""

  def get_move(self, state: ds.BoardState) -> ds.Move:
    moves = state.get_valid_moves()

    # If we can cure, make that as likely as moving.
    if any([isinstance(move, ds.CureMove) for move in moves]):
      for i in range(len(moves) - 2):
        moves.append(ds.CureMove())

    return random.choice(moves)


class CurePolicy(Policy):
  """If we can cure, do. Otherwise move randomly."""

  def get_move(self, state: ds.BoardState) -> ds.Move:
    moves = state.get_valid_moves()
    if any([isinstance(move, ds.CureMove) for move in moves]):
      return ds.CureMove()
    return random.choice(moves)
