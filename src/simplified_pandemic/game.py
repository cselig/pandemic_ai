import logging

import interfaces
import simplified_pandemic.data_structures as ds


def play_game(actor: interfaces.Policy) -> int:
  state = ds.BoardState()

  logging.debug(state)
  while not state.is_terminal():
    move = actor.get_move(state)
    logging.debug(move)
    state.make_move(move)
    logging.debug(state)

  if state.is_won():
    logging.info("You won!")
    return 1
  else:
    logging.info("You lost :(")
    return 0
