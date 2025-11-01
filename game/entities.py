import pygame
from config import *

class Ghost:
    def __init__(self, pos, color, personality='Blinky'):
        self.pos = pos
        self.startPos = pos
        self.color = color

        # 4 ghosts in Pacman
        # Blinky
        # Pinky
        # Inky
        # Clyde

        # How can I define each personality?
        # Which algorithm is more suited for this
        self.personality = personality

        # scared triggers when power pellet
        self.scared = False
        self.state = 'normal' # normal, scared, dead

def displayPacman(surface, pos):
    pr, pc = pos
    rect = pygame.Rect(pc * cellSize + 2, pr * cellSize + 2, cellSize - 4, cellSize - 4)
    pygame.draw.circle(surface, pacmanColor, rect.center, cellSize // 2 - 4)

def displayGhost(surface, pos, color):
    gr, gc = pos
    rect = pygame.Rect(gc * cellSize + 3, gr * cellSize + 3, cellSize - 6, cellSize - 6)
    pygame.draw.ellipse(surface, color, rect)

def displayFood(surface, pos_or_set, power_set=None):
    if isinstance(pos_or_set, (list, set)):
        for (fr, fc) in pos_or_set:
            rect = pygame.Rect(fc * cellSize + 6, fr * cellSize + 6, cellSize - 12, cellSize - 12)
            pygame.draw.ellipse(surface, foodColor, rect)

    elif pos_or_set is None:
        return
    
    else:
        fr, fc = pos_or_set
        rect = pygame.Rect(fc * cellSize + 4, fr * cellSize + 4, cellSize - 8, cellSize - 8)
        pygame.draw.ellipse(surface, foodColor, rect)

    # power pellets drawn differently if provided
    if power_set:
        for (pr, pc) in power_set:
            rect = pygame.Rect(pc * cellSize + 4, pr * cellSize + 4, cellSize - 8, cellSize - 8)
            pygame.draw.circle(surface, scaredGhostColor, rect.center, (cellSize // 2) - 6)
