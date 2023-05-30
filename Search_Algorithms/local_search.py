def hill_climbing_search(problem, start, end):
    current = start
    while True:
        neighbors = problem.actions(current)
        best_neighbor = current
        for neighbor in neighbors:
            if problem.cost(current, neighbor) < problem.cost(current, best_neighbor):
                best_neighbor = neighbor
        if problem.cost(current, best_neighbor) >= problem.cost(current, end):
            return None
        if problem.is_goal(best_neighbor):
            return [best_neighbor]
        current = best_neighbor

