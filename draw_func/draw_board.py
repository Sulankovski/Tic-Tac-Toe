import pygame
import numpy as np
import numpy.typing as npt


def draw_board(rows: int, columns: int, grid: npt.NDArray[np.int16]) -> None:
    """


    :param rows: number of rows
    :param columns: number of columns
    :param grid: game grid
    :return: None
    """
    pygame.init()
    width, height = 300, 300
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("X O")

    screen.fill((255, 255, 255))

    cell_size = width // columns
    line_thickness = 3

    for i in range(rows + 1):
        y = i * cell_size
        pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y), line_thickness)

    for i in range(rows):
        for j in range(columns):
            x = j * cell_size
            y = i * cell_size

            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height), line_thickness)

            if grid[i, j] == 1:
                pygame.draw.line(screen, (0, 0, 0), (x + 0.2 * cell_size, y + 0.2 * cell_size),
                                 (x + 0.8 * cell_size, y + 0.8 * cell_size), line_thickness)
                pygame.draw.line(screen, (0, 0, 0), (x + 0.2 * cell_size, y + 0.8 * cell_size),
                                 (x + 0.8 * cell_size, y + 0.2 * cell_size), line_thickness)
            elif grid[i, j] == 2:
                pygame.draw.circle(screen, (0, 0, 0), (x + cell_size // 2, y + cell_size // 2),
                                   cell_size // 2 - int(0.1 * cell_size), line_thickness)
    pygame.display.flip()


def show_board(rows: int, columns: int, grid: npt.NDArray[np.int16]) -> None:
    """

    :param rows: number of rows
    :param columns: number of columns
    :param grid: game grid
    :return: None
    """
    for i in range(0, rows):
        for j in range(0, columns):
            if grid[i, j] == 0:
                print(' _ ', end='')

            elif grid[i, j] == 1:
                print(' X ', end='')

            else:
                print(' O ', end='')

        print()
