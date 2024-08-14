import abc
import enum
import logging
import random
from dataclasses import dataclass

MAX_TURNS = 15
SUBTURNS = 2
MAX_OUTBREAKS = 3
OUTBREAK_THRESHOLD = 3


class City(enum.IntEnum):
  SONOMA = 1
  BERKELEY = 2
  OAKLAND = 3
  HAYWARD = 4
  PLEASANTON = 5
  FREMONT = 6
  SAN_JOSE = 7
  SUNNYVALE = 8
  LOS_ALTOS = 9
  SAN_MATEO = 10
  SAN_FRANCISCO = 11
  SAUSALITO = 12
  NAPA = 13


city_graph = {
  City.SONOMA: [City.BERKELEY, City.NAPA],
  City.BERKELEY: [City.SONOMA, City.OAKLAND, City.NAPA],
  City.OAKLAND: [City.BERKELEY, City.NAPA, City.HAYWARD],
  City.HAYWARD: [City.OAKLAND, City.SAN_MATEO, City.PLEASANTON],
  City.PLEASANTON: [City.HAYWARD, City.FREMONT],
  City.FREMONT: [City.HAYWARD, City.PLEASANTON, City.SAN_JOSE],
  City.SAN_JOSE: [City.FREMONT, City.SUNNYVALE],
  City.SUNNYVALE: [City.SAN_JOSE, City.LOS_ALTOS, City.SAN_MATEO],
  City.LOS_ALTOS: [City.SAN_MATEO, City.SUNNYVALE],
  City.SAN_MATEO: [City.SUNNYVALE, City.LOS_ALTOS, City.SAN_FRANCISCO],
  City.SAN_FRANCISCO: [City.SAN_MATEO, City.SAUSALITO, City.NAPA],
  City.SAUSALITO: [City.SAN_FRANCISCO, City.NAPA],
  City.NAPA: [City.SAN_FRANCISCO, City.SAUSALITO, City.SONOMA, City.BERKELEY, City.OAKLAND],
}


class Move(abc.ABC):
  pass


@dataclass
class CureMove(Move):
  pass


@dataclass
class LocationMove(Move):
  destination: City


@dataclass
class BoardState:
  pawn1_location: City
  pawn2_location: City
  infection_counts: dict[City, int]
  player_turn: int    # 1 or 2
  turn_number: int    # 1 to 5
  subturn_number: int # 1 to 4
  outbreak_count: int # 0 to 3

  def __init__(self):
    # initial infections
    self.infection_counts = {c: 0 for c in City}
    self.infect(4)

    self.pawn1_location = City.SAN_FRANCISCO
    self.pawn2_location = City.SAN_FRANCISCO
    self.player_turn = 1
    self.turn_number = 1
    self.subturn_number = 1
    self.outbreak_count = 0

  def infect(self, n = 1):
    for _ in range(n):
      city = random.choice(list(City))
      logging.debug("infecting: %s", city.name)
      self.infection_counts[city] += 1

  def current_player_location(self) -> City:
    return self.pawn1_location if self.player_turn == 1 else self.pawn2_location

  def is_won(self):
    return self.turn_number >= MAX_TURNS

  def is_lost(self):
    return self.outbreak_count >= MAX_OUTBREAKS

  def is_terminal(self):
    return self.is_won() or self.is_lost()

  def get_valid_moves(self) -> list[Move]:
    moves = [LocationMove(c) for c in city_graph[self.current_player_location()]]
    if self.infection_counts[self.current_player_location()] > 0:
      moves.append(CureMove())
    return moves

  def make_move(self, move: Move):
    if isinstance(move, CureMove):
      assert self.infection_counts[self.current_player_location()] > 0
      self.infection_counts[self.current_player_location()] -= 1
    elif isinstance(move, LocationMove):
      assert move.destination in city_graph[self.current_player_location()]
      if self.player_turn == 1:
        self.pawn1_location = move.destination
      elif self.player_turn == 2:
        self.pawn2_location = move.destination
      else:
        raise ValueError()
    else:
      raise NotImplementedError()

    # increment turn numbers
    self.subturn_number += 1
    if self.subturn_number == SUBTURNS:
      self.subturn_number = 1
      self.player_turn = 1 if self.player_turn == 2 else 2
      if self.player_turn == 1:
        self.turn_number += 1

    city_to_infect = random.choice(list(City))
    if self.infection_counts[city_to_infect] < OUTBREAK_THRESHOLD:
      self.infection_counts[city_to_infect] += 1
    else:
      self._do_outbreak(city_to_infect, set([city_to_infect]))

  def _do_outbreak(self, city: City, outbroken_cities: set[City]):
    self.outbreak_count += 1
    for neighbor in city_graph[city]:
      if neighbor in outbroken_cities:
        continue
      if self.infection_counts[neighbor] < OUTBREAK_THRESHOLD:
        self.infection_counts[neighbor] += 1
      else:
        outbroken_cities.add(neighbor)
        self._do_outbreak(neighbor, outbroken_cities)

  def __str__(self):
    result = [
      '',
      f'Player turn: {self.player_turn}',
      f'Subturn: {self.subturn_number}',
      f'Turn: {self.turn_number}',
      f'Outbreak count: {self.outbreak_count}',
      f'Player 1 location: {self.pawn1_location.name}',
      f'Player 2 location: {self.pawn2_location.name}',
      '',
    ]
    for city in sorted(self.infection_counts.keys()):
      if self.infection_counts[city] > 0:
        result.append(f'{city.name}: {self.infection_counts[city]}')
    return '\n'.join(result)
