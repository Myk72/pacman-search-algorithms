import pygame
from config import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption("Pacman Game")
    font = pygame.font.SysFont("comicsansms", 17)
    clock = pygame.time.Clock()
    
    return []


if __name__ == "__main__":
    main()
