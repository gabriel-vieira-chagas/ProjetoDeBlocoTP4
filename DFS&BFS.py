from collections import deque


class UndirectedGraph:
    def __init__(self):
        self.adjacency = {}

    def add_node(self, node):
        if node not in self.adjacency:
            self.adjacency[node] = []

    def connect(self, u, v):
        if u in self.adjacency:
            self.adjacency[u].append(v)
        else:
            self.adjacency[u] = [v]
        if v in self.adjacency:
            self.adjacency[v].append(u)
        else:
            self.adjacency[v] = [u]

    def depth_first_all_paths(self, start, end):
        if start not in self.adjacency or end not in self.adjacency:
            return []
        results = []
        visited = {start}

        def _dfs(current, path):
            if current == end:
                results.append(path[:])
                return
            for neighbor in self.adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    _dfs(neighbor, path)
                    path.pop()
                    visited.remove(neighbor)

        _dfs(start, [start])
        return results

    def shortest_path_bfs(self, start, end):
        if start not in self.adjacency or end not in self.adjacency:
            return []
        if start == end:
            return [start]
        queue = deque([[start]])
        seen = {start}
        while queue:
            path = queue.popleft()
            node = path[-1]
            for neighbor in self.adjacency[node]:
                if neighbor not in seen:
                    new_path = path + [neighbor]
                    if neighbor == end:
                        return new_path
                    seen.add(neighbor)
                    queue.append(new_path)

        return []


g = UndirectedGraph()
g.add_node('A')
g.add_node('B')
g.add_node('C')
g.add_node('D')
g.add_node('E')

g.connect('A', 'B')
g.connect('A', 'C')
g.connect('B', 'D')
g.connect('C', 'D')
g.connect('C', 'E')
g.connect('D', 'E')

print("DFS de A para D:")
print(g.depth_first_all_paths('A', 'D'))

print("\nBFS de A para E:")
print(g.shortest_path_bfs('A', 'E'))