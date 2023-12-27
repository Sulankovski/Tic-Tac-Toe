def get_input(user_input: str) -> tuple:
    """

    :param user_input: user_input
    :return: parsed row and column
    """
    row = user_input.split(" ")[0]
    column = user_input.split(" ")[1]

    return int(row), int(column)
