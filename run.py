import pygame, sys
from config import *
from game.maze import MazeLayout
from game.entities import displayPacman, displayGhost, displayFood, Ghost
# from game.utils import manhattan, eculidean
from game.search import SearchAlgorithm
from game.gameplay import minimaxMode

def main():
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Pacman Game")
    font = pygame.font.SysFont("comicsansms", 17)
    clock = pygame.time.Clock()

    pacmanMaze = MazeLayout(SIMPLE_MAP_SEARCH)
    startingPoint = pacmanMaze.startPoint
    print(startingPoint, 'strt pt')
    
    ghosts = [Ghost(p, c) for p, c in zip(pacmanMaze.ghosts, [ghostColor, ghostColor2, ghostColor3, ghostColor4])]
    # foods = [
    
    food = pacmanMaze.food # 1 food for search and many for minimax
    power = pacmanMaze.power # 0 power pellets for search and 2 - 3 for minimax
 
    searchProcess = None
    visited, frontSet = set(), set()
    path = []

    mode, algorithm = "neutral", ""
    status = "Press 1-4 to run BFS/DFS/UCS/A*. Press M for Minimax gameplay. R to reset"
    orginalStat = status

    while True:
        clock.tick(fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:

                # Minimax Gameplay cmd
                if e.key == pygame.K_m:
                    minimaxMode(MazeLayout(SIMPLE_MAP_MINIMAX), screen, font)
                
                # Reset cmd
                elif e.key == pygame.K_r:
                    pacmanMaze = MazeLayout(SIMPLE_MAP_SEARCH)
                    startingPoint = pacmanMaze.startPoint
                    ghosts = [Ghost(p, c) for p, c in zip(pacmanMaze.ghosts, [ghostColor, ghostColor2, ghostColor3, ghostColor4])]
                    food = pacmanMaze.food
                    power = pacmanMaze.power
                    visited, frontSet, path = set(), set(), []
                    status = orginalStat
                
                # I have separated search and minimax modes

                # Search algorithm cmds
                elif e.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    keys = {pygame.K_1 : 'BFS', pygame.K_2: 'DFS', pygame.K_3: 'UCS',pygame.K_4: 'A*'}
                    # print(keys[e.key], "here deb")
                    # print(SearchAlgorithm[keys[e.key]], 'searhc')
                    # algorthm, func = SearchAlgorithm[keys[e.key]]
                    algorithm = keys[e.key]
                    SearchFunc = SearchAlgorithm[algorithm]
                    
                    # min(food, key=lambda x: manhattan(startingPoint, x))

                    if isinstance(food, set):
                        goal = next(iter(food))
                    else:
                        goal = food
                    
                    visited, frontSet, path = set(), set(), []
                    searchProcess = SearchFunc(pacmanMaze, startingPoint, goal)

                    mode = "search"
                    status = f'Currently seletced {algorithm}'
                   

        if mode == "search":
            try:
                kind, cell = next(searchProcess)
                if kind == "explore": 
                    visited.add(cell)
                elif kind == "open": 
                    frontSet.add(cell)
                elif kind == "path": 
                    path.append(cell)
                elif kind == "done": 
                    mode = "neutral"
            except StopIteration:
                mode = "neutral"

        screen.fill(backgroundColor )
        pacmanMaze.displayGrid(screen)

        for c in frontSet:
            pygame.draw.rect(screen, frontierColor, (c[1]*cellSize, c[0]*cellSize, cellSize, cellSize))

        for c in visited:
            pygame.draw.rect(screen, exploredColor, (c[1]*cellSize, c[0]*cellSize, cellSize, cellSize))

        for c in path:
            pygame.draw.rect(screen, pathColor, (c[1]*cellSize, c[0]*cellSize, cellSize, cellSize))

        # pellets
        displayFood(screen, food, power)

        for g in ghosts:
            displayGhost(screen, g.pos, g.color)

        displayPacman(screen, startingPoint)

        pygame.draw.rect(screen, (20,20,20), (0, gridRows*cellSize, windowWidth, statusHeight))

        txt = font.render(status, True, textColor)
        screen.blit(txt, (10, gridRows * cellSize + 10))
        pygame.display.flip()


if __name__ == "__main__":
    main()
