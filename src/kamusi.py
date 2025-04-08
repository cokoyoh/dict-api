class TrieNode:
  def __init__(self):
    self.children = {}
    self.is_end_of_word = False
    self.definitions = []

class Trie:
  def __init__(self):
    self.root = TrieNode() 
  
  def insert(self, word, definitions=None):
    current = self.root
    for char in word:
      if char not in current.children:
        current.children[char] = TrieNode()
      current = current.children[char]
    current.is_end_of_word = True
    if definitions:
      current.definitions.extend(definitions)

  def search(self, word):
    current = self.root 
    for char in word:
      if char not in current.children:
        return None
      current = current.children[char]
    return current

  def _find_node(self, prefix):
    current = self.root
    for char in prefix:
      if char not in current.children:
        return None
      current = current.children[char]
    return current 

  def _dfs(self, node, prefix, results):    
    if node.is_end_of_word:
      results.append({ "word": prefix, "definitions": node.definitions })
    for char, child_node in node.children.items():
      self._dfs(child_node, prefix + char, results)

  def autocomplete(self, prefix):
    results = []
    node = self._find_node(prefix)
    if node is not None:
      self._dfs(node, prefix, results)
    return results
