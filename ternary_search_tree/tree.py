
class Node:

    def __init__(self, char):
        self._char = char
        self._lt, self._eq, self._gt, self._string = None, None, None, None
        self._terminates = False


    def _insert(self, string, index):
        current = string[index]
        print(current)
        if current < self._char:
            if self._lt is None:
                self._lt = Node(string[index])
            self._lt._insert(string, index)
        elif current > self._char:
            if self._gt is None:
                self._gt = Node(string[index])
            self._gt._insert(string, index)
        else:
            if self._eq is None:
                self._eq = Node(string[index])
            if index + 1 < len(string):
                self._eq._insert(string, index + 1)
            else:
                self._string = string
                self._terminates = True

    def __repr__(self):
        if not self._char:
            return f"terminates: {self._terminates}"
        return f"char: {self._char}, terminates: {self._terminates}"



class TernarySearchTree:

    def __init__(self):
        self._root: Node = Node('')
        self._size = 0

    def insert(self, string):
        if len(string) == 0:
            if self._root._terminates is False:
                self._size = self._size + 1
            self._root._terminates = True
            self._root._string = string
        else:
            self._root = self._insert(self._root, 0, string)
            self._size = self._size + 1

    def _insert(self, node, index, string):
        if index == len(string):
            return
        current = string[index]
        if node is None:
            node = Node(current)
        if current < node._char:
            node._lt = self._insert(node._lt, index, string)
        elif current > node._char:
            node._gt = self._insert(node._gt, index, string)
        else:
            node._eq = self._insert(node._eq, index + 1, string)
            if index + 1 == len(string):
                node._terminates = True
                node._string = string

        return node

    def __len__(self):
        return self._size

    def __repr__(self):
        lines = []

        def _recurse(node: Node, child: str, prefix: str) -> None:
            if node is None:
                return

            lines.append(f"{child}{prefix}{node}")

            if node._lt:
                _recurse(node._lt, "_lt", "  " + prefix)
            if node._eq:
                _recurse(node._eq, "_eq", "  " + prefix)
            if node._gt:
                _recurse(node._gt, "_gt", "  " + prefix)

        _recurse(self._root, "", "")

        return "\n".join(lines)

    def all_strings(self):
        strings = []

        def _dfs(node):
            if node is None:
                return
            _dfs(node._lt)
            if node._terminates:
                strings.append(node._string)
            _dfs(node._eq)
            _dfs(node._gt)

        _dfs(self._root)

        return strings

    def search(self, string):
        node = self._root
        index = 0
        while node is not None:
            current = string[index]
            if current < node._char:
                node = node._lt
            elif current > node._char:
                node = node._gt
            elif current == node._char:
                if index == len(string) - 1:
                    return True
                index += 1
                node = node._eq
            else:
                return False

        return False