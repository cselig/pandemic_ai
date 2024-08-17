import abc


class Move(abc.ABC):
  pass


class BoardState(abc.ABC):
  def is_won(self) -> bool:
    raise NotImplementedError()

  def is_lost(self) -> bool:
    raise NotImplementedError()

  def is_terminal(self) -> bool:
    # No draws for now.
    return self.is_won() or self.is_lost()

  def get_valid_moves(self) -> list[Move]:
    raise NotImplementedError()

  def make_move(self, move: Move):
    raise NotImplementedError()


class Policy(abc.ABC):
  @abc.abstractmethod
  def get_move(self, state: BoardState) -> Move:
    raise NotImplementedError()
