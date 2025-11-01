from heapq import heappush, heappop
from collections import deque
from config import *
from .utils import *

# BFS ALGORITHM
def bfs(grid, start, goal):
    que = deque([start])
    vis = {start: None}

    while que:
        curr = que.popleft()
        yield ('explore', curr)
        if curr == goal:
            # print('basecase', curr)
            # return tracePath(vis, goal)
            yield from tracePath(vis, goal)
            return
        
        for x, y in neighbors(curr):
            if grid.isClear((x, y)) and (x, y) not in vis:
                vis[(x, y)] = curr
                que.append((x, y))
                yield ('open', (x, y))

        # print('vis bfs', vis)
    # return []
    yield ('done', [])


# DFS ALGORITHM
def dfs(grid, start, goal):
    stack = [start]
    vis = {start: None}

    while stack:
        curr = stack.pop()
        yield ('explore', curr)
        if curr == goal:
            # print('dfs here', current)
            # return tracePath(vis, goal)
            yield from tracePath(vis, goal)
            return
        
        # for x, y in [()]
        for x, y in neighbors(curr):
            if grid.isClear((x, y)) and (x, y) not in vis:
                vis[(x, y)] = curr
                stack.append((x, y))
                yield ('open', (x, y))

    # return []
    yield ('done', [])


# UCS ALGORITHM
def ucs(grid, start, goal):
    # BFS + Priority Queue
    heap = [(0, start)]
    vis = {start: None}
    costs = {start: 0}

    while heap:
        cost, curr = heappop(heap)

        yield ('explore', curr)
        if curr == goal:
            yield from tracePath(vis, goal)
            return
        
        for x, y in neighbors(curr):
            if grid.isClear((x, y)):
                new_cost = cost + 1
                if (x, y) not in costs or new_cost < costs[(x, y)]:
                    costs[(x, y)] = new_cost
                    vis[(x, y)] = curr
                    heappush(heap, (new_cost, (x, y)))
                    yield ('open', (x, y))

    yield ('done', [])





# A* ALGORITHM
def astar(grid, start, goal):
    # UCS + Heuristic
    # In this case, I used Manhattan distance as heuristic
    # we could also use Euclidean distance

    heap = [(manhattan(start, goal), start)]
    vis = {start: None}
    g = {start: 0} 

    while heap:
        f, curr = heappop(heap)
        yield ('explore', curr)
        if curr == goal:
            # return tracePath(vis, goal)
            yield from tracePath(vis, goal)
            return
        
        for x, y in neighbors(curr):
            if grid.isClear((x, y)):
                new_g = g[curr] + 1
                if (x, y) not in g or new_g < g[(x, y)]:
                    g[(x, y)] = new_g
                    f = new_g + manhattan((x, y), goal)
                    heappush(heap, (f, (x, y)))
                    vis[(x, y)] = curr
                    yield ('open', (x, y))
    # return []
    yield ('done', [])


def tracePath(vis, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = vis[node]
    path.reverse()
    for cell in path:
        yield ('path', cell)
    return path


SearchAlgorithm = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "A*": astar
}
