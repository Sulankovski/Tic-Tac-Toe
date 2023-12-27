import numpy as np

import numpy.typing as npt


def empty_fields(grid: npt.NDArray[np.int16]) -> int:
    """

    :param grid: game grid
    :return: count of empty fields
    """
    count = 0
    for row in range(3):
        for column in range(3):
            if grid[row][column] == 0:
                count += 1
    return count
