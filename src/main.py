import logging

from simplified_pandemic import game
from simplified_pandemic import policies


def main():
  logging.basicConfig(level=logging.DEBUG)

  logging.info('Running!')

  total_games = 100
  won_games = 0

  policy = policies.TreeSearchPolicy(3)
  # policy = policies.CurePolicy()
  # policy = policies.RandomPolicy()

  for _ in range(total_games):
    won_games += game.play_game(policy)

  logging.info(f'You won {won_games} out of {total_games}.')


if __name__ == '__main__':
  main()
