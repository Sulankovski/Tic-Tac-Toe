import numpy as np
import numpy.typing as npt


def check_game_over(grid: npt.NDArray[np.int16]) -> bool:
    """

    :param grid:game grid
    :return: bool
    """
    for i in range(3):
        if check_column(i, grid):
            return True
        if check_row(i, grid):
            return True
    if check_primary_diagonal(grid):
        return True
    if check_secondary_diagonal(grid):
        return True

    return False


def check_column(column: int, grid: npt.NDArray[np.int16]) -> bool:
    flag = True
    for i in range(3):
        if grid[i][column] == 0:
            flag = False
    return grid[0][column] == grid[1][column] == grid[2][column] and flag


def check_row(row: int, grid: npt.NDArray[np.int16]) -> bool:
    flag = True
    for i in range(3):
        if grid[row][i] == 0:
            flag = False
    return grid[row][0] == grid[row][1] == grid[row][2] and flag


def check_primary_diagonal(grid: npt.NDArray[np.int16]) -> bool:
    flag = True
    for i in range(3):
        for j in range(3):
            if i == j and grid[i][j] == 0:
                flag = False
    return grid[0][0] == grid[1][1] == grid[2][2] and flag


def check_secondary_diagonal(grid: npt.NDArray[np.int16]) -> bool:
    flag = True
    for i in range(3):
        for j in range(3):
            if i + j == 2 and grid[0][i] == 0:
                flag = False
    return grid[2][0] == grid[1][1] == grid[0][2] and flag


def check_move(row: int, column: int, row_num: int, column_num: int, grid: npt.NDArray[np.int16]) -> bool:
    """

    :param row: row to check
    :param column: column to check
    :param row_num: number of rows
    :param column_num: number of columns
    :param grid: game grid
    :return: bool
    """
    if row < 0 or row >= row_num or column < 0 or column >= column_num or grid[row, column] != 0:
        return False

    return True
