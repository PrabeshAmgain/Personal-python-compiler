import collections
import heapq
import math

# Node positions for heuristic calculation
node_positions = {
    'A': (1, 1), 'B': (2.5, 1), 'C': (1, 2.5),
    'D': (4, 1), 'E': (2.5, 2.5), 'F': (1, 4),
    'G': (2.5, 4)
}

def bfs(graph, start, goal):
    """
    Performs Breadth-First Search on a graph.

    Args:
        graph: A dictionary representing the graph's adjacency list.
        start: The starting node.
        goal: The goal node.

    Returns:
        A tuple containing:
            - A list of nodes in the path from start to goal.
            - A list of visited nodes in the order they were visited.
    """
    visited = []
    queue = collections.deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            visited.append(node)
            if node == goal:
                return path, visited

            for neighbor, weight in graph.get(node, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None, visited

def dfs(graph, start, goal):
    """
    Performs Depth-First Search on a graph.

    Args:
        graph: A dictionary representing the graph's adjacency list.
        start: The starting node.
        goal: The goal node.

    Returns:
        A tuple containing:
            - A list of nodes in the path from start to goal.
            - A list of visited nodes in the order they were visited.
    """
    visited = []
    stack = [(start, [start])]

    while stack:
        (node, path) = stack.pop()

        if node not in visited:
            visited.append(node)
            if node == goal:
                return path, visited

            for neighbor, weight in reversed(graph.get(node, [])):
                stack.append((neighbor, path + [neighbor]))

    return None, visited

def euclidean_distance(node1, node2):
    """
    Calculates the Euclidean distance between two nodes.
    """
    pos1 = node_positions[node1]
    pos2 = node_positions[node2]
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def a_star(graph, start, goal, heuristic):
    """
    Performs A* Search on a graph.

    Args:
        graph: A dictionary representing the graph's adjacency list.
               The graph should have weights for each edge.
        start: The starting node.
        goal: The goal node.
        heuristic: A function that takes two nodes and returns an estimated
                   cost to the goal.

    Returns:
        A tuple containing:
            - A list of nodes in the path from start to goal.
            - A list of visited nodes in the order they were visited.
    """
    visited = []
    # (priority, cost, path)
    priority_queue = [(0 + heuristic(start, goal), 0, [start])]

    while priority_queue:
        (_, cost, path) = heapq.heappop(priority_queue)
        node = path[-1]

        if node not in visited:
            visited.append(node)
            if node == goal:
                return path, visited

            for neighbor, weight in graph.get(node, []):
                new_cost = cost + weight
                priority = new_cost + heuristic(neighbor, goal)
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(priority_queue, (priority, new_cost, new_path))

    return None, visited

# A simple graph represented as an adjacency list.
# The keys are the nodes, and the values are lists of tuples,
# where each tuple contains a neighbor and the weight of the edge.
sample_graph = {
    'A': [('B', 1), ('C', 3)],
    'B': [('A', 1), ('D', 5), ('E', 2)],
    'C': [('A', 3), ('F', 2)],
    'D': [('B', 5)],
    'E': [('B', 2), ('F', 1)],
    'F': [('C', 2), ('E', 1), ('G', 4)],
    'G': [('F', 4)]
}
