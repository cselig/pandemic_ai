import logging

from simplified_pandemic import game
from simplified_pandemic import policies


def main():
  logging.basicConfig(level=logging.INFO)

  logging.info('Running!')

  total_games = 100
  won_games = 0

  for _ in range(total_games):
    won_games += game.play_game(policies.CurePolicy())

  logging.info(f'You won {won_games} out of {total_games}.')


if __name__ == '__main__':
  main()
