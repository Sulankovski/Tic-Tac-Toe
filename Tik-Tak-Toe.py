import random

import numpy as np
from copy import copy

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
heuristic_table[2, 0] = 15


def show_board():
    # Iterate over each row and column in the board
    for i in range(0, rows):
        for j in range(0, columns):
            # Print the corresponding symbol based on the value in the board
            if grid[i, j] == 0:
                print(' _ ', end='')

            elif grid[i, j] == 1:
                print(' X ', end='')

            else:
                print(' O ', end='')

        # Move to the next line to print the next row
        print()


def check_game_over():
    for i in range(3):
        if check_column(i):
            return True
        if check_row(i):
            return True
    if check_primary_diagonal():
        return True
    if check_secondary_diagonal():
        return True

    return False


def check_column(column):
    flag = True
    for i in range(3):
        if grid[i][column] == 0:
            flag = False
    return grid[0][column] == grid[1][column] == grid[2][column] and flag


def check_row(row):
    flag = True
    for i in range(3):
        if grid[row][i] == 0:
            flag = False
    return grid[row][0] == grid[row][1] == grid[row][2] and flag


def check_primary_diagonal():
    flag = True
    for i in range(3):
        for j in range(3):
            if i == j and grid[i][j] == 0:
                flag = False
    return grid[0][0] == grid[1][1] == grid[2][2] and flag


def check_secondary_diagonal():
    flag = True
    for i in range(3):
        for j in range(3):
            if i + j == 2 and grid[0][i] == 0:
                flag = False
    return grid[2][0] == grid[1][1] == grid[0][2] and flag


def check_move(row, column):
    if row < 0 or row >= rows or column < 0 or column >= columns or grid[row, column] != 0:
        return False

    return True


def state_value(state):
    flaten_state = copy(state.ravel())
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


def minimax(state, alpha, beta, find_max, empty_spaces, ai_value, human_value):
    if empty_spaces == 0:
        return state_value(state), state

    rows_left, columns_left = np.where(state == 0)
    state_to_edit = copy(state)

    if rows_left.shape[0] == 0:
        return state_value(state), state_to_edit

    if find_max:
        value = _min
        for i in range(rows_left.shape[0]):
            new_state = copy(state)
            new_state[rows_left[i], columns_left[i]] = ai_value

            new_value, _ = minimax(new_state, alpha, beta, False, empty_spaces - 1, ai_value, human_value)

            if new_value > value:
                value = new_value
                state_to_edit = copy(new_state)

            if value > alpha:
                alpha = value

            if alpha >= beta:
                break
        return value, state_to_edit

    else:
        value = _max
        for i in range(rows_left.shape[0]):
            new_state = copy(state)
            new_state[rows_left[i], columns_left[i]] = human_value

            new_value, _ = minimax(new_state, alpha, beta, True, empty_spaces - 1, ai_value, human_value)

            if new_value < value:
                value = new_value
                state_to_edit = copy(new_state)

            if value < beta:
                beta = value

            if alpha >= beta:
                break

        return value, state_to_edit


def get_input(user_input):
    row = user_input.split(" ")[0]
    column = user_input.split(" ")[1]

    return int(row), int(column)


def human__vs__ai():
    global grid
    player_on_move = random.randint(1, 3)
    possible_plays = 9

    while possible_plays > 0:
        if player_on_move == 1:
            print('Your turn')
            player_on_move = 0

            move = False
            while not move:
                try:
                    new_row, new_column = get_input(input("Input row and column: "))
                except:
                    move = False
                if check_move(new_row - 1, new_column - 1):
                    grid[new_row - 1, new_column - 1] = 1
                    move = True
                else:
                    print('Invalid move!')

            show_board()

            if check_game_over():
                print('Human win')
                return
        else:
            print('AI turn')
            player_on_move = 1

            state = np.copy(grid)
            spaces_left = np.sum(state == 0)
            value, new_state = minimax(state, _min, _max, True, spaces_left, 2, 1)
            grid = np.copy(new_state)

            show_board()

            if check_game_over():
                print("AI wins")
                return
        possible_plays -= 1

    print("Draw")


if __name__ == "__main__":
    human__vs__ai()