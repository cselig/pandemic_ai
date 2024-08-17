import copy
import logging
import random

import interfaces
import simplified_pandemic.data_structures as ds


class RandomPolicy(interfaces.Policy):
  """Makes a random move."""

  def get_move(self, state: ds.BoardState) -> interfaces.Move:
    moves = state.get_valid_moves()

    # If we can cure, make that as likely as moving.
    if any([isinstance(move, ds.CureMove) for move in moves]):
      for i in range(len(moves) - 2):
        moves.append(ds.CureMove())

    return random.choice(moves)


class CurePolicy(interfaces.Policy):
  """If we can cure, do. Otherwise move randomly."""

  def get_move(self, state: ds.BoardState) -> interfaces.Move:
    moves = state.get_valid_moves()
    if any([isinstance(move, ds.CureMove) for move in moves]):
      return ds.CureMove()
    return random.choice(moves)


class TreeSearchNode:
  def __init__(self, board_state: ds.BoardState, precursor_move: interfaces.Move | None = None):
    self.board_state = board_state
    # The move that was made to get to this state.
    self.precursor_move = precursor_move
    self.children: list[TreeSearchNode] = []
    self.parent: TreeSearchNode | None = None
    self.min_value_in_subtree: int | None = None

  def expand(self, depth: int):
    self.expand_recursively(depth)
    self.compute_min_value_in_subtree()

  def compute_min_value_in_subtree(self):
    if not self.children:
      self.min_value_in_subtree = self.board_state.get_value()
    else:
      for child in self.children:
        child.compute_min_value_in_subtree()
      self.min_value_in_subtree = min([c.min_value_in_subtree for c in self.children])

  def expand_recursively(self, depth: int):
    if depth == 0:
      return

    moves = self.board_state.get_valid_moves()
    if isinstance(moves[0], ds.InfectMove):
      moves = [ds.InfectCityMove(city=c) for c in ds.City]
    for move in moves:
      child_state = copy.deepcopy(self.board_state)
      child_state.make_move(move)
      child_node = TreeSearchNode(child_state, move)
      child_node.expand_recursively(depth - 1)
      self.children.append(child_node)

  def select_best_move(self) -> interfaces.Move:
    max_min_value = -9999999
    best_move = None
    for child in self.children:
      logging.debug(f'Child has value: {child.min_value_in_subtree}, {child.precursor_move}')
      if child.min_value_in_subtree > max_min_value:
        max_min_value = child.min_value_in_subtree
        best_move = child.precursor_move
    if best_move is None:
      raise ValueError()
    return best_move


class TreeSearchPolicy(interfaces.Policy):
  """Perform a naive tree search to select the next action."""

  def __init__(self, max_depth: int):
    self.max_depth = max_depth

  def get_move(self, state: ds.BoardState) -> interfaces.Move:
    search_node = TreeSearchNode(state)
    search_node.expand(self.max_depth)
    move = search_node.select_best_move()
    logging.debug(f'Tree search selecting: {move}')
    return move
