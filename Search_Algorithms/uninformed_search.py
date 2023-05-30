def depth_first_search(problem, start, end):
    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in problem.actions(node):
                stack.append((neighbor, path + [neighbor]))

    return []

def breadth_first_search(problem, start, end):
    visited = set()
    queue = [(start, [start])]

    while queue:
        node, path = queue.pop(0)
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in problem.actions(node):
                queue.append((neighbor, path + [neighbor]))

    return []

def uniform_cost_search(problem, start, end):
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
                queue.sort(key=lambda x: x[2])  # Sort the queue based on path cost

    return []

def depth_limited_search(problem, start, end, depth_limit):
    return recursive_dls(start, end, problem, [start], depth_limit)

def recursive_dls(node, end, problem, path, depth_limit):
    if node == end:
        return path

    if depth_limit == 0:
        return []

    cutoff_occurred = False

    for neighbor in problem.actions(node):
        if neighbor not in path:
            result = recursive_dls(neighbor, end, problem, path + [neighbor], depth_limit - 1)
            if result == 'cutoff':
                cutoff_occurred = True
            elif result:
                return result

    if cutoff_occurred:
        return 'cutoff'
    else:
        return []
