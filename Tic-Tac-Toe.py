import random
import numpy as np
import numpy.typing as npt
import copy
import pygame
import sys

from draw_func.draw_board import draw_board, show_board
from helper_func.check_for_winner import check_game_over, check_move
from helper_func.empty_fields import empty_fields
from helper_func.input import get_input

rows = 3
columns = 3
win_combinations = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]])
_max = float('inf')
_min = float('-inf')
grid = np.zeros((rows, columns))

heuristic_table = np.zeros((rows + 1, columns + 1))
for index in range(0, rows + 1):
    heuristic_table[index, 0] = 2 ** index
    heuristic_table[0, index] = -2 ** index
heuristic_table[1, 1] = 10
heuristic_table[2, 2] = 20
heuristic_table[3, 3] = 15


def state_value(state: npt.NDArray[np.int16]) -> int:
    """

    :param state: present game state
    :return: best heuristic value
    """
    flaten_state = copy.deepcopy(state.ravel())
    heuristic = 0

    for i in range(8):
        o_win_occurrences = 0
        x_win_occurrences = 0
        for j in range(3):
            if flaten_state[win_combinations[i, j]] == 2:
                o_win_occurrences += 1
            elif flaten_state[win_combinations[i, j]] == 1:
                x_win_occurrences += 1

        heuristic += heuristic_table[o_win_occurrences][x_win_occurrences]

    return heuristic


def minimax(state: npt.NDArray[np.int16], alpha: float, beta: float, find_max: bool, empty_spaces: int) -> tuple:
    """

    :param state: present game state
    :param alpha: minimum val
    :param beta: maximum val
    :param find_max: define maximizer or minimizer
    :param empty_spaces: spaces left
    :param ai_value: 2
    :param human_value: 1
    :return: heuristic value, new state
    """
    rows_left, columns_left = np.where(state == 0)
    state_to_edit = copy.deepcopy(state)

    if empty_spaces == 0:
        return state_value(state=state), state

    if rows_left.shape[0] == 0:
        return state_value(state=state), state_to_edit

    if find_max:
        value = _min
        for i in range(rows_left.shape[0]):
            new_state = copy.deepcopy(state)
            new_state[rows_left[i], columns_left[i]] = 2

            new_value, _ = minimax(state=new_state, alpha=alpha, beta=beta, find_max=False, empty_spaces=empty_spaces-1)

            if new_value > value:
                value = new_value
                state_to_edit = copy.deepcopy(new_state)

            if value > alpha:
                alpha = value

            if alpha >= beta:
                break

        return value, state_to_edit

    else:
        value = _max
        for i in range(rows_left.shape[0]):
            new_state = copy.deepcopy(state)
            new_state[rows_left[i], columns_left[i]] = 2

            new_value, _ = minimax(state=new_state, alpha=alpha, beta=beta, find_max=True, empty_spaces=empty_spaces-1)

            if new_value < value:
                value = new_value
                state_to_edit = copy.deepcopy(new_state)

            if value < beta:
                beta = value

            if alpha >= beta:
                break

        return value, state_to_edit


def human__vs__ai(flag: bool) -> None:
    """

    :param flag: which interface to use
    :return: game results
    """
    global grid
    player_on_move = random.randint(1, 3)
    possible_plays = 9
    new_row, new_column = 0, 0

    while possible_plays > 0 and not check_game_over(grid=grid) and empty_fields(grid=grid) != 0:
        if flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        if player_on_move == 1:
            print('Your turn')
            player_on_move = 0

            move = False
            while not move:
                try:
                    new_row, new_column = get_input(input("Input row and column: "))
                except:
                    move = False
                if check_move(row=new_row - 1, column=new_column - 1, row_num=rows, column_num=columns, grid=grid):
                    grid[new_row - 1, new_column - 1] = 1
                    move = True
                else:
                    print('Invalid move!')

            draw_board(rows=rows, columns=columns, grid=grid) \
                if flag else (
                show_board(rows=rows, columns=columns, grid=grid))


            if check_game_over(grid=grid):
                print('Human win')
                return
        else:
            print('AI turn')
            player_on_move = 1

            state = np.copy(grid)
            spaces_left = np.sum(state == 0)
            value, new_state = minimax(state=state, alpha=_min, beta=_max, find_max=False, empty_spaces=spaces_left)
            grid = np.copy(new_state)

            draw_board(rows=rows, columns=columns, grid=grid) \
                if flag else (
                show_board(rows=rows, columns=columns, grid=grid))

            if check_game_over(grid=grid):
                print("AI wins")
                return
        possible_plays -= 1

    print("Draw")


def human__vs__ai__game(interface: str):
    """

    :param interface: Interface to use
    """
    if interface == "pygame":
        while True:
            if not check_game_over(grid=grid) and empty_fields(grid=grid) != 0:
                draw_board(rows=rows, columns=columns, grid=grid)
                human__vs__ai(flag=True)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
    elif interface == "cmd":
        human__vs__ai(flag=False)


if __name__ == '__main__':
    print("Choose interface: ")
    print("Choose _ 1 _ for _ pygame _ or _ 2 _ for _ cmd _ interface")
    num = input()
    human__vs__ai__game(interface="pygame") if num == 1 else human__vs__ai__game(interface="cmd")
