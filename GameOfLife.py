# -*- coding: utf-8 -*-
"""Game of life gamejam, 6.6.21."""

import pygame
import numpy as np
import time
import os
import csv

class Grid:
    """
    Class to store information about game of life instance.

    __init__; creates grid Data
    iterate: puts system through one tick
    """

    def __init__(self, size, periodic):
        """
        Initialise game of life data.

        size = [x,y]
        periodic = Boolean: if not, then edges are deadspace
        """
        self.data = np.zeros(size)
        self.size = size
        self.periodic = periodic

    def iterate(self):
        """
        Iterate through one tick.

        Uses periodic attribute to determine behaviour.
        """
        if self.periodic is True:
            # create proxy matrix with edge pieces for periodicity
            proxy = np.concatenate([self.data[None, self.size[0]-1, :],
                                    self.data, self.data[None, 0, :]])

            proxy = np.concatenate([proxy[:, self.size[1]-1, None], proxy,
                                   proxy[:, 0, None]], 1)

        else:
            # create proxy matrix with white edges for periodicity
            proxy = np.concatenate(np.zeros(self.size[0]-1, 1), self.data,
                                   np.zeros(self.size[0]-1, 1))
            proxy = np.concatenate(np.zeros(1, self.size[1]+1), proxy,
                                   np.zeros(1, self.size[1]+1))

        for x in range(1, self.size[0]+1):
            for y in range(1, self.size[1]+1):
                NeighbourSum = np.sum(proxy[x-1:x+2,
                                      y-1:y+2]) - proxy[x, y]
                if NeighbourSum == 2:
                    print(NeighbourSum)
                    print(proxy[x,y])
                elif NeighbourSum == 2 and proxy[x, y] == 1:
                    pass
                elif NeighbourSum == 3:
                    self.data[x-1, y-1] = 1
                else:
                    self.data[x-1, y-1] = 0

    def save(self,filename):
        """
        Save current instance of game of life.

        filename should end with .csv.
        """
        with open(filename, 'w', newline='') as f:
            # create the csv writer
            writer = csv.writer(f)

            # write a row to the csv file
            print(self.data)
            writer.writerows(np.ndarray.tolist(self.data))

    def load(self,filename):
        pass

    def random(self):
        """
        randomise current instance of game of life.
        """
        self.data = np.round(np.random.random_sample([self.size[0],
                                                      self.size[1]]))


def main():
    """
    Create game instance for interacting with game of life.

    click to toggle a cell.
    spacebar starts iterations.
    + increases iteration rate.
    - decreases iteration rate.
    r randomises state.
    backspace clears state.
    s saves current state.
    """
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("game of life")

    size = [50,50]
    GridEmpty = Grid(size, True)
    iterating = False
    tickrate = 1
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((15*size[0], 15*size[1]))
    livingcell = pygame.image.load("filledcell.png")
    bgd_image = pygame.image.load("background.png")
    # define a variable to control the main loop
    running = True
    # main loop
    while running:
        screen.blit(bgd_image, (0, 0))
        # render living cells
        for x in range(GridEmpty.size[0]):
            for y in range(GridEmpty.size[1]):
                if GridEmpty.data[x, y] == True:
                    screen.blit(livingcell, (15*x, 15*y))
        pygame.display.flip()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            print(event)
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # changes state of pressed cell
                cellx = int(event.pos[0]/15)
                celly = int(event.pos[1]/15)
                GridEmpty.data[cellx, celly] = not(GridEmpty.data[cellx, celly])

            if event.type == pygame.KEYDOWN:
                # toggles iteration and starts timer for first tick
                if event.unicode == ' ':
                    if iterating is False:
                        t0 = time.perf_counter()
                    iterating = not(iterating)
                if event.unicode == '+':
                    # increases tickrate
                    tickrate = 1.5*tickrate
                    print(tickrate)
                if event.unicode == '-':
                    # decreases tickrate
                    tickrate = tickrate / 1.5
                    print(tickrate)
                if event.key == 8:
                    #clears grid
                    GridEmpty.data = np.zeros([GridEmpty.size[0], GridEmpty.size[1]])
                if event.unicode == 'r':
                    #generates random Grid
                    GridEmpty.random()
                if event.unicode == 's':
                    print(pygame.key.get_pressed())
                    pass
                    suffix = 1
                    save_path = 'SavedData' + str(suffix) + '.csv'
                    while os.path.exists(save_path) is True:
                        suffix += 1
                        save_path = 'SavedData' + str(suffix) + '.csv'

                    open(save_path, 'x')
                    GridEmpty.save(save_path)
                if event.key == 27:
                    running = False

        if iterating is True:
            if time.perf_counter() > t0 + 1/tickrate:
                t0 += 1/tickrate
                GridEmpty.iterate()

if __name__ == "__main__":
    # call the main function
    main()
