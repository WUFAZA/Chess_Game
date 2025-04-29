import pygame as pg
import pyautogui


class Tool(object):

    def __init__(self, name, color, pos, player):
        self.player = player
        self.name = name
        self.team = color  # 0 = white, 1 = black
        self.position = pos
        self.icon = None
        self.x = 0
        self.y = 0
        self.two_move = False
        self.just_now = False

    def is_legal_move(self, op):
        on_board = 0 <= op[1] < 8 and 0 <= op[0] < 8

        # Makes sure the move does not result in a chess (or mate in case there is a check already)
        def good_for_king():
            ignore = None
            old_pos = self.position.copy()
            self.position = op
            for e in self.player.enemy.tools:
                if e.position == op:
                    ignore = e
                    break
            good = not self.player.is_checked(ignore)
            self.position = old_pos
            return good

        return on_board and good_for_king()

    def handle_castle(self, pos):
        if type(self) == King and abs(self.position[1] - pos[1]) == 2:
            self.player.castles = [False, False, False]
            if pos[1] == 2 and self.player.castles[:2]:
                self.player.tools[6].move([pos[0], 3])
            elif pos[1] == 6 and self.player.castles[1:]:
                self.player.tools[7].move([pos[0], 5])
        elif type(self) == Rook:
            if self.position[1] == 0:
                self.player.castles[0] = False
            elif self.position[1] == 7:
                self.player.castles[2] = False

    def pawn_two_moves(self, pos):
        for t in self.player.tools + self.player.enemy.tools:
            if type(t) == Pawn:
                self.just_now = False
        if abs(self.position[0] - pos[0]) == 2:
            self.two_move = False
            self.just_now = True

    def eat(self, pos):
        for t in self.player.enemy.tools:
            # Normal piece eating move
            if t.position == pos:
                t.position = None
            # En-Passent piece eating move
            if type(self) == type(t) == Pawn:
                # White pawn eating a black one
                if self.team == 0:
                    if [pos[0] + 1, pos[1]] == t.position and t.just_now:
                        t.position = None
                # Black pawn eating a white one
                elif self.team == 1:
                    if [pos[0] - 1, pos[1]] == t.position and t.just_now:
                        t.position = None

    def handle_coronation(self):
        if type(self) == Pawn and self.position[0] == self.team * 7:
            choice = pyautogui.confirm(text="What is the piece you want instead of the pawn?", title="coronation",
                                       buttons=["Bishop", "Knight", "Queen", "Rook"])
            if choice == "Bishop":
                self.player.tools[self.player.tools.index(self)] = Bishop(
                    "Extra " + "white " * (1 - self.team) + "black " * self.team + "bishop", self.team, self.position,
                    self.player)
            elif choice == "Knight":
                self.player.tools[self.player.tools.index(self)] = Knight(
                    "Extra " + "white " * (1 - self.team) + "black " * self.team + "knight", self.team, self.position,
                    self.player)
            elif choice == "Queen":
                self.player.tools[self.player.tools.index(self)] = Queen(
                    "Extra " + "white " * (1 - self.team) + "black " * self.team + "queen", self.team, self.position,
                    self.player)
            elif choice == "Rook":
                self.player.tools[self.player.tools.index(self)] = Rook(
                    "Extra " + "white " * (1 - self.team) + "black " * self.team + "rook", self.team, self.position,
                    self.player)

    def move(self, pos):
        self.player.since_pawn_move += 1
        self.handle_castle(pos)
        self.pawn_two_moves(pos)
        self.position = pos
        if type(self) == Pawn:
            self.two_move = False
            self.player.since_pawn_move = 0
        elif type(self) == King:
            self.player.castles[1] = False
        self.eat(pos)
        self.handle_coronation()
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94

    def show(self, screen):
        screen.blit(self.icon, (self.x, self.y))


class Pawn(Tool):

    def __init__(self, name, color, pos, player):
        Tool.__init__(self, name, color, pos, player)
        if color == 0:
            self.icon = pg.image.load(r"Img\white_pawn.png")
        else:
            self.icon = pg.image.load(r"Img\black_pawn.png")
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94
        self.two_move = True
        self.just_now = False

    def valid_move(self, pos_to_check, ignore=None):
        ps = [i.position for i in self.player.enemy.tools]
        enemies_at = self.player.enemy.tools.copy()
        ans = False
        # White pawn
        if self.team == 0:
            # One step forward
            if self.position[0] - pos_to_check[0] == 1:
                if abs(pos_to_check[1] - self.position[1]) == 1:
                    ans = pos_to_check in ps or \
                          len(list(filter(lambda x: x.just_now and x.position == [pos_to_check[0] + 1,
                                                                                  pos_to_check[1]], enemies_at))) > 0
                elif pos_to_check[1] == self.position[1]:
                    ans = pos_to_check not in ps
            # 2 steps forward
            elif self.position[0] - pos_to_check[0] == 2:
                if pos_to_check[1] == self.position[1]:
                    ans = pos_to_check not in ps and [pos_to_check[0] + 1, pos_to_check[1]] not in ps and self.two_move
        # Black Pawn
        else:
            if pos_to_check[0] - self.position[0] == 1:
                if abs(pos_to_check[1] - self.position[1]) == 1:
                    ans = pos_to_check in ps or \
                          len(list(filter(lambda x: x.just_now and x.position == [pos_to_check[0] - 1,
                                                                                  pos_to_check[1]], enemies_at))) == 1
                elif pos_to_check[1] == self.position[1]:
                    ans = pos_to_check not in ps
            elif pos_to_check[0] - self.position[0] == 2:
                if pos_to_check[1] == self.position[1]:
                    ans = pos_to_check not in ps and [pos_to_check[0] - 1, pos_to_check[1]] not in ps and self.two_move
        return ans


class Rook(Tool):

    def __init__(self, name, color, pos, player):
        Tool.__init__(self, name, color, pos, player)
        if color == 0:
            self.icon = pg.image.load(r"Img\white_rook.png")
        else:
            self.icon = pg.image.load(r"Img\black_rook.png")
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94

    def valid_move(self, pos_to_check, ignore=None):
        if self.position == pos_to_check:
            return False
        eps = [t.position for t in self.player.enemy.tools]
        fps = [t.position for t in self.player.tools if t != ignore]
        if self.position[0] == pos_to_check[0]:
            for i in range(min(self.position[1], pos_to_check[1]) + 1, max(self.position[1], pos_to_check[1])):
                if [self.position[0], i] in eps + fps:
                    return False
        elif self.position[1] == pos_to_check[1]:
            for i in range(min(self.position[0], pos_to_check[0]) + 1, max(self.position[0], pos_to_check[0])):
                if [i, self.position[1]] in eps + fps:
                    return False
        else:
            return False
        if pos_to_check not in fps:
            return True
        return False


class Bishop(Tool):

    def __init__(self, name, color, pos, player):
        Tool.__init__(self, name, color, pos, player)
        if color == 0:
            self.icon = pg.image.load(r"Img\white_bishop.png")
        else:
            self.icon = pg.image.load(r"Img\black_bishop.png")
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94

    def valid_move(self, pos_to_check, ignore=None):
        if abs(self.position[0] - pos_to_check[0]) != abs(self.position[1] - pos_to_check[1]):
            return False
        dx = pos_to_check[1] - self.position[1]
        dy = pos_to_check[0] - self.position[0]
        fps = [t.position for t in self.player.tools if t != ignore]
        eps = [t.position for t in self.player.enemy.tools]
        if dx == dy:
            for i in range(min(self.position[1], pos_to_check[1]) + 1, max(self.position[1], pos_to_check[1])):
                if [self.position[0] - self.position[1] + i, i] in eps + fps:
                    return False
        elif dx + dy == 0:
            for i in range(min(self.position[1], pos_to_check[1]) + 1, max(self.position[1], pos_to_check[1])):
                if [self.position[1] + self.position[0] - i, i] in eps + fps:
                    return False
        if pos_to_check not in fps:
            return True
        return False


class Queen(Tool):

    def __init__(self, name, color, pos, player):
        Tool.__init__(self, name, color, pos, player)
        if color == 0:
            self.icon = pg.image.load(r"Img\white_queen.png")
        else:
            self.icon = pg.image.load(r"Img\black_queen.png")
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94

    def valid_move(self, pos_to_check, ignore=None):
        if self.position is None:
            return False
        r = Rook(self.name, self.team, self.position, self.player).valid_move(pos_to_check, ignore)
        b = Bishop(self.name, self.team, self.position, self.player).valid_move(pos_to_check, ignore)
        return r or b


class King(Tool):

    def __init__(self, name, color, pos, player):
        Tool.__init__(self, name, color, pos, player)
        if color == 0:
            self.icon = pg.image.load(r"Img\white_king.png")
        else:
            self.icon = pg.image.load(r"Img\black_king.png")
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94

    def castle_pos(self, pos_to_check):
        castles = False
        poses = []
        if self.team == 0:
            if pos_to_check == [7, 2] and all(self.player.castles[:2]):
                poses = [[7, 2], [7, 3], [7, 4]]
                castles = True
            if pos_to_check == [7, 6] and all(self.player.castles[1:]):
                poses = [[7, 4], [7, 5], [7, 6]]
                castles = True
        elif self.team == 1:
            if pos_to_check == [0, 2] and all(self.player.castles[:2]):
                poses = [[0, 2], [0, 3], [0, 4]]
                castles = True
            if pos_to_check == [0, 6] and all(self.player.castles[1:]):
                poses = [[0, 4], [0, 5], [0, 6]]
                castles = True
        if castles:
            if all([not t.valid_move(p) for p in poses for t in self.player.enemy.tools if t.position is not None]):
                return True

    def valid_move(self, pos_to_check, ignore=None):
        if self.castle_pos(pos_to_check):
            return True
        possibilities = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == j == 0) and pos_to_check not in [i.position for i in self.player.tools if
                                                              i.position is not None]:
                    possibilities.append([self.position[0] + i, self.position[1] + j])
        return pos_to_check in possibilities


class Knight(Tool):

    def __init__(self, name, color, pos, player):
        Tool.__init__(self, name, color, pos, player)
        if color == 0:
            self.icon = pg.image.load(r"Img\white_knight.png")
        else:
            self.icon = pg.image.load(r"Img\black_knight.png")
        self.x = 14 + self.position[1] * 94
        self.y = 14 + self.position[0] * 94

    def valid_move(self, pos_to_check, ignore=None):
        d = (abs(pos_to_check[0] - self.position[0]) == 2 and abs(pos_to_check[1] - self.position[1]) == 1) or \
            (abs(pos_to_check[0] - self.position[0]) == 1 and abs(pos_to_check[1] - self.position[1]) == 2)
        f = len([t for t in self.player.tools if t.position == pos_to_check and t != ignore]) == 0
        return d and f