
class Node:

    def __init__(self, char):
        self._char = char
        self._lt, self._eq, self._gt, self._string = None, None, None, None
        self._terminates = False


    def __repr__(self):
        if not self._char:
            return f"terminates: {self._terminates}"
        return f"char: {self._char}, terminates: {self._terminates}"



class TernarySearchTree:

    def __init__(self):
        self._root: Node = Node('')

    def insert(self, string):
        if len(string) == 0:
            self._root._terminates = True
            self._root._string = string
        else:
            self._root = self._insert(self._root, 0, string)

    def _insert(self, node, index, string):
        current = string[index]
        if node is None:
            node = Node(current)
        if current < node._char:
            node._lt = self._insert(node._lt, index, string)
        elif current > node._char:
            node._gt = self._insert(node._gt, index, string)
        else:
            if index + 1 == len(string):
                node._terminates = True
                node._string = string
            else:
                node._eq = self._insert(node._eq, index + 1, string)

        return node

    def __len__(self):
        return len(self.all_strings())

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

    def search(self, string, exact=False):
        if len(string) == 0:
            if exact:
                return self._root._terminates
            else:
                return True
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
                    if exact:
                        return node._string == string
                    return True
                index += 1
                node = node._eq
            else:
                return False

        return False
