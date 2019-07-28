from cell import Cell
from desease import Desease
from map_r import Map
from sir import Sir_Model

from itertools import product
from random import shuffle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import pygame

SUSCEPTIBLE = "S"
INFECTIOUS = "I"
RECOVERED = "R"

SUSCEPTIBLE_COLOR = (0,0,255)
INFECTIOUS_COLOR = (255,0,0)
RECOVERED_COLOR = (0,255,0)

def fullfill_map(x_len, y_len, sir):
    possible_positions = list(product(range(x_len), range(y_len)))
    shuffle(possible_positions)
    population = len(possible_positions)
    susceptibles = [Cell(SUSCEPTIBLE, *i) for i in possible_positions[:(int(sir.H))]]
    infecteds = [Cell(INFECTIOUS, *i) for i in possible_positions[(int(sir.H)):]]
    return susceptibles, infecteds


def main():

    GRID_SIZE = (110, 100)

    sir = Sir_Model()
    susceptibles, infecteds = fullfill_map(GRID_SIZE[0], GRID_SIZE[1], sir)

    neighborhood_function = Desease.r_1

    cells = susceptibles + infecteds
    desease = Desease(4, 10, neighborhood_function, 2)


    map_1 = Map(GRID_SIZE[0], GRID_SIZE[1], cells, desease, sir)
    
    
    # This sets the WIDTH and HEIGHT of each grid location
    BLOCK_SIZE = 5
    
    # Initialize pygame
    pygame.init()
    
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [GRID_SIZE[0] * BLOCK_SIZE, GRID_SIZE[1] * BLOCK_SIZE]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Cholera")
    
    # Loop until the user clicks the close button.
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                map_1.next_t()
                print("next t")
    
        # Set the screen background
        screen.fill(RECOVERED_COLOR)
        
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                color = RECOVERED_COLOR
                if map_1.map[(i, j)].state == SUSCEPTIBLE:
                    color = SUSCEPTIBLE_COLOR
                if map_1.map[(i, j)].state == INFECTIOUS:
                    color = INFECTIOUS_COLOR
                pygame.draw.rect(screen,
                                color,
                                [(BLOCK_SIZE) * i,
                                (BLOCK_SIZE) * j,
                                BLOCK_SIZE,
                                BLOCK_SIZE])

    
        # Limit to 60 frames per second
        clock.tick(60)
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()