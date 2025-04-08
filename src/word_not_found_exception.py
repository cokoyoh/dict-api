class WordNotFound(Exception):
  def __init__(self, query: str):
    self.query = query
