import heapq

# Manhattan directions only
DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def turn_penalty(prev_dir, new_dir):
    if prev_dir == new_dir:
        return 0
    return 20

def astar_manhattan(cost_grid, start, goal):
    """
    Direction-aware A*.
    start, goal = (x, y)
    """

    h, w = cost_grid.shape

    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    open_set = []
    heapq.heappush(open_set, (0, (*start, 0, 0)))
    came_from = {}
    g_score = {(*start, 0, 0): 0}

    while open_set:
        _, (x, y, dx, dy) = heapq.heappop(open_set)

        if (x, y) == goal:
            return reconstruct_path(came_from, (x,y,dx,dy))

        for ndx, ndy in DIRS:
            nx, ny = x + ndx, y + ndy
            if not (0 <= nx < w and 0 <= ny < h):
                continue

            step_cost = cost_grid[ny][nx]
            if step_cost >= 1e5:
                continue

            bend = turn_penalty((dx,dy), (ndx,ndy))
            new_cost = g_score[(x,y,dx,dy)] + step_cost + bend

            state = (nx, ny, ndx, ndy)
            if new_cost < g_score.get(state, float("inf")):
                g_score[state] = new_cost
                priority = new_cost + heuristic((nx,ny), goal)
                heapq.heappush(open_set, (priority, state))
                came_from[state] = (x,y,dx,dy)

    return []

def reconstruct_path(came_from, state):
    path = [(state[0], state[1])]
    while state in came_from:
        state = came_from[state]
        path.append((state[0], state[1]))
    return path[::-1]
