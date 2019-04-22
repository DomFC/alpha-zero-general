from string import ascii_uppercase
from checkers.Board import _1D_to_2D_board

DIM = 8
whitespace_prefix = ' ' * 10
coordinates_list = list(ascii_uppercase)[:DIM]
coordinates_dict = {letter:ind for ind, letter in enumerate(coordinates_list)}
upper_lines = '┌' + ('───┬' * (DIM - 1)) + '───┐'
middle_lines = '├' + ('───┼' * (DIM - 1)) + '───┤'
bottom_lines = '└' + ('───┴' * (DIM - 1)) + '───┘'

def char_to_print(c):
    if c == 1:
        return 'w'
    if c == 2:
        return 'W'
    if c == -1:
        return 'b'
    if c == -2:
        return 'B'
    return ' '

def display(_1D_board):
    board = _1D_to_2D_board(_1D_board)
    print()

    # Print horizontal coordinates
    print(whitespace_prefix, end='   ')
    for coord in coordinates_list:
        print('  {} '.format(coord), end='')
    print()
    print(whitespace_prefix, ' ', upper_lines)

    for y in range(DIM):
        print(whitespace_prefix, coordinates_list[y], end=' ')
        for x in range(DIM):
            print('│ ', char_to_print(board[y][x]), ' ', end='', sep='')
        print('│')
        if y != DIM - 1:
            print(whitespace_prefix, ' ', middle_lines)
    print(whitespace_prefix, ' ', bottom_lines)
