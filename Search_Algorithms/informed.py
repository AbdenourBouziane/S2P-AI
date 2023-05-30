import sys

def greedy_best_first_search(problem, start, end, heuristic):
    visited = set()
    queue = [(start, [start])]

    while queue:
        node, path = queue.pop(0)
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            neighbors = problem.actions(node)
            neighbors.sort(key=lambda n: heuristic(n, end))  # Sort the neighbors based on heuristic value
            for neighbor in neighbors:
                queue.append((neighbor, path + [neighbor]))

    return []


def a_star_search(problem, start, end, heuristic):
    visited = set()
    queue = [(start, [start], 0)]

    while queue:
        node, path, cost = queue.pop(0)
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in problem.actions(node):
                new_cost = cost + problem.cost(node, neighbor)
                queue.append((neighbor, path + [neighbor], new_cost))
                queue.sort(key=lambda x: x[2] + heuristic(x[0], end))  # Sort the queue based on f(n) = g(n) + h(n)

    return []


def hill_climbing_search(problem, start, end, heuristic):
    current = start

    while current != end:
        neighbors = problem.actions(current)
        neighbors.sort(key=lambda n: heuristic(n, end))
        next_node = neighbors[0]  # Choose the neighbor with the lowest heuristic value
        if heuristic(next_node, end) >= heuristic(current, end):
            break  # If the next node doesn't improve the heuristic value, stop
        current = next_node

    if current == end:
        return [start, end]  # Return the path from start to end if a solution is found
    else:
        return []  # Return an empty path if no solution is found


def iterative_deepening_a_star(problem, start, end, heuristic):
    for depth_limit in range(sys.maxsize):
        result = recursive_dls_a_star(start, end, problem, [start], depth_limit, float('inf'), heuristic)
        if result:
            return result

    return []


def recursive_dls_a_star(node, end, problem, path, depth_limit, cost_limit, heuristic):
    if node == end:
        return path

    if depth_limit == 0:
        return []

    cutoff_occurred = False

    for neighbor in problem.actions(node):
        new_cost = problem.cost(node, neighbor) + heuristic(neighbor, end)
        if new_cost <= cost_limit:
            result = recursive_dls_a_star(
                neighbor, end, problem, path + [neighbor], depth_limit - 1, cost_limit - new_cost, heuristic
            )
            if result == 'cutoff':
                cutoff_occurred = True
            elif result:
                return result

    if cutoff_occurred:
        return 'cutoff'
    else:
        return []
