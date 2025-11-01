from config import *

class MazeLayout:
    def __init__(self, layout):
        
        self.grid = layout
        self.startPoint = None

        # food pellets 
        self.food = set()

        # power pellets (set)
        self.power = set()

        self.ghosts = []
        self.ghostsHome = None

        for row, row_list in enumerate(layout):
            for col, char in enumerate(row_list):
                if char == 'P':
                    self.startPoint = (row, col)
                elif char == 'F':
                    self.food.add((row, col))
                elif char == 'O' or char == 'o':
                    self.power.add((row, col))
                elif char == 'G':
                    self.ghosts.append((row, col))
                    if self.ghostsHome is None:
                        self.ghostsHome = (row, col)

        if not self.startPoint:
            raise ValueError("Layout must have start position 'P'")
        
        # Fallback ghost house
        # if not self.ghost_house and self.ghosts:
        #     self.ghost_house = self.ghosts[0]
        

    def isClear(self, pos):
        r, c = pos
        return 0 <= r < gridRows and 0 <= c < gridCols and self.grid[r][c] != '#'

    def displayGrid(self, surface):
        for r in range(gridRows):
            for c in range(gridCols):
                rect = pygame.Rect(c * cellSize, r * cellSize, cellSize, cellSize)
                color = wallColor if self.grid[r][c] == '#' else openCellColor
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, gridColor, rect, 1)
