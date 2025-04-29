from Tools import *


class Player(object):

    def __init__(self, color):
        king = [King("White " * (1 - color) + "Black " * color + "King", color, [7 - 7 * color, 4], self)]
        queen = [Queen("White " * (1 - color) + "Black " * color + "Queen", color, [7 - 7 * color, 3], self)]
        bishops = [Bishop("White " * (1 - color) + "Black " * color + "Bishop 1", color, [7 - 7 * color, 2], self),
                   Bishop("White " * (1 - color) + "Black " * color + "Bishop 2", color, [7 - 7 * color, 5], self)]
        knights = [Knight("White " * (1 - color) + "Black " * color + "Knight 1", color, [7 - 7 * color, 1], self),
                   Knight("White " * (1 - color) + "Black " * color + "Knight 2", color, [7 - 7 * color, 6], self)]
        rooks = [Rook("White " * (1 - color) + "Black " * color + "Rook 1", color, [7 - 7 * color, 0], self),
                 Rook("White " * (1 - color) + "Black " * color + "Rook 2", color, [7 - 7 * color, 7], self)]
        pawns = [Pawn("White " * (1 - color) + "Black " * color + "Pawn " + str(i + 1), color, [6 - 5 * color, i], self)
                 for i in range(8)]
        self.team = color
        self.name = "Player %d (%s)" % (color, "white" * (1 - color) + "black" * color)
        self.tools = king + queen + bishops + knights + rooks + pawns
        self.enemy = None
        self.castles = [True, True, True]
        self.since_pawn_move = 0

    def is_checked(self, to_ignore=None):
        king_pos = self.tools[0].position.copy()
        for t in self.enemy.tools:
            if t != to_ignore:
                if t.position is not None and t.valid_move(king_pos, to_ignore):
                    return True
        return False