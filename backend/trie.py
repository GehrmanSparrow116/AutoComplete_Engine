"""Trie Data Structure Implementation"""
import heapq
from typing import List, Dict, Tuple, Optional


class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end: bool = False
        self.frequency: int = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self._total_words = 0
        self._total_nodes = 1

    def insert(self, word: str, frequency: int = 1) -> None:
        if not word or not isinstance(word, str):
            return
        word = word.lower().strip()
        if not word:
            return

        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
                self._total_nodes += 1
            current = current.children[char]

        if not current.is_end:
            current.is_end = True
            self._total_words += 1

        current.frequency += frequency

    def search(self, word: str) -> Optional[int]:
        if not word or not isinstance(word, str):
            return None
        word = word.lower().strip()
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        return current.frequency if current.is_end else None

    def delete(self, word: str) -> bool:
        if not word or not isinstance(word, str):
            return False
        word = word.lower().strip()

        def _delete_helper(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.frequency = 0
                self._total_words -= 1
                return len(node.children) == 0

            char = word[depth]
            if char not in node.children:
                return False

            should_delete_child = _delete_helper(node.children[char], word, depth + 1)

            if should_delete_child:
                del node.children[char]
                self._total_nodes -= 1
                return len(node.children) == 0 and not node.is_end

            return False

        return _delete_helper(self.root, word, 0)

    def autocomplete(self, prefix: str, top_k: int = 10) -> List[Dict]:
        if not prefix or not isinstance(prefix, str):
            return []
        prefix = prefix.lower().strip()

        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        heap: List[Tuple[int, str]] = []

        def _dfs(node: TrieNode, current_word: str) -> None:
            if node.is_end:
                entry = (-node.frequency, current_word)
                if len(heap) < top_k:
                    heapq.heappush(heap, entry)
                elif entry > heap[0]:
                    heapq.heapreplace(heap, entry)

            for char, child_node in node.children.items():
                _dfs(child_node, current_word + char)

        _dfs(current, prefix)

        results = []
        while heap:
            freq, word = heapq.heappop(heap)
            results.append({"word": word, "frequency": -freq})
        results.reverse()
        return results

    def stats(self) -> Dict[str, int]:
        return {
            "total_words": self._total_words,
            "total_nodes": self._total_nodes,
            "trie_depth": self._calculate_depth()
        }

    def _calculate_depth(self) -> int:
        def _depth_helper(node: TrieNode) -> int:
            if not node.children:
                return 0
            return 1 + max(_depth_helper(child) for child in node.children.values())
        return _depth_helper(self.root)

    def get_all_words(self) -> List[Tuple[str, int]]:
        words = []
        def _dfs(node: TrieNode, current_word: str) -> None:
            if node.is_end:
                words.append((current_word, node.frequency))
            for char, child_node in node.children.items():
                _dfs(child_node, current_word + char)
        _dfs(self.root, "")
        return words
