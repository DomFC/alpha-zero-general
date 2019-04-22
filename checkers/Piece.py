from enum import IntEnum

class Piece(IntEnum):
    BLACK = -1
    BLACK_KING = -2
    WHITE = 1
    WHITE_KING = 2
    NONE = 0

all_pieces = {
    Piece.BLACK: 'b',
    Piece.BLACK_KING: 'B',
    Piece.WHITE: 'w',
    Piece.WHITE_KING: 'W',
    Piece.NONE: ' ',
}

def char_val(piece):
    return all_pieces[piece]
