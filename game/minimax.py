from config import *
from .utils import manhattan, neighbors
import random

def availablePath(grid, pos):
    path = []
    for x, y in neighbors(pos):
        if grid.isClear((x, y)):
            path.append((x, y))
    return path

def utility(pac, ghost, food):
    if pac == ghost:
        return utilityCatch
    
    if pac in food:
        return utilityGoal
    
    # nearestFood = min(manhattan(pac, f) for f in food)
    ghostDist = manhattan(pac, ghost)
    return ghostDist
    # return 2 * nearestFood - 3 * ghostDist


def minimax_decision(gridmap, ghostPos, pac, food, depth=minimaxDepth):

    def maximize(pacPos, ghost_pos, d, alpha, beta):
        if pacPos == ghost_pos:
            return utilityCatch
        if pacPos in food:
            return utilityGoal
        
        if d == 0:
            return utility(pacPos, ghost_pos, food)

        v = float('-inf')
        for move in availablePath(gridmap, pacPos):
            v = max(v, minimize(move, ghost_pos, d - 1, alpha, beta))
            alpha = max(alpha, v)

            if alpha >= beta:
                break
        return v

    def minimize(pacPos, ghost_pos, d, alpha, beta):
        if pacPos == ghost_pos:
            return utilityCatch
        if pacPos in food:
            return utilityGoal
        if d == 0:
            return utility(pacPos, ghost_pos, food)

        v = float('inf')
        for move in availablePath(gridmap, ghost_pos):
            v = min(v, maximize(pacPos, move, d - 1, alpha, beta))
            beta = min(beta, v)

            if alpha >= beta:
                break
        return v

    bestMove = ghostPos
    bestValue = float('inf')
    alpha, beta = float('-inf'), float('inf')
    moves = availablePath(gridmap, ghostPos)
    if not moves:
        return ghostPos

    random.shuffle(moves) 

    for move in moves:
        val = maximize(pac, move, depth - 1, alpha, beta)
        if val < bestValue:
            bestValue, bestMove = val, move
        beta = min(beta, bestValue)

    return bestMove