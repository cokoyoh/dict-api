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
        node = self._find_node(word)
        if node and node.is_end_of_word:
            return {"word": word, "definitions": node.definitions}
        return None

    def _find_node(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return None
            current = current.children[char]
        return current

    def _dfs(self, node, prefix, results):
        if node.is_end_of_word:
            results.append({"word": prefix, "definitions": node.definitions})
        for char, child_node in node.children.items():
            self._dfs(child_node, prefix + char, results)

    def autocomplete(self, prefix):
        results = []
        node = self._find_node(prefix)
        if node is not None:
            self._dfs(node, prefix, results)
        return results
    
    def delete(self, word): 
        def _delete(node, word, depth):
            if not node:
                return None

            if depth == len(word):
                if node.is_end_of_word:
                    node.is_end_of_word = False
                    if not node.children:
                        return None
                return node

            char = word[depth]
            if char in node.children:
                child_node = _delete(node.children[char], word, depth + 1) 
                if child_node is None:
                    del node.children[char]
                    if not node.children and not node.is_end_of_word:
                        return None
            return node

        _delete(self.root, word, 0)
