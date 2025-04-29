from Player import *


class Game(object):

    def __init__(self):
        self.player1 = Player(0)
        self.player2 = Player(1)
        self.player2.enemy = self.player1
        self.player1.enemy = self.player2

    # Return "t" if there is no mate option for both players, a list of both players' movable tools
    def available(self):
        # List of player one's tools that can move
        p1 = [t for t in self.player1.tools if t.position is not None]
        # List of player two's tools that can move
        p2 = [t for t in self.player2.tools if t.position is not None]
        # Return "t" if there is no mate option
        if (len(p1) == len(p2) == 0) or \
           (len(p1) == 1 and len(p2) == 0) and (type(p1[0]) == Knight or type(p1[0]) == Bishop) or \
           (len(p2) == 1 and len(p1) == 0) and (type(p2[0]) == Knight or type(p2[0]) == Bishop):
            return "t"
        # Return list of movable tools for each player
        return [p1, p2]

    def is_over(self):
        movables = self.available()
        if movables == "t":
            return "Tie"
        # Gets the amount of moves each player is able to perform
        p1_movements = 0
        p2_movements = 0
        for l in range(8):
            for c in range(8):
                for x in movables[0]:
                    if x.valid_move([l, c]) and x.is_legal_move([l, c]):
                        p1_movements += 1
                for y in movables[1]:
                    if y.valid_move([l, c]) and y.is_legal_move([l, c]):
                        p2_movements += 1
        # If player 1 is under check and none of his tools can move, player 2 won
        if self.player1.is_checked():
            if p1_movements == 0:
                return self.player2.name
        # If player 2 is under check and none of his tools can move, player 1 won
        elif self.player2.is_checked():
            if p2_movements == 0:
                return self.player1.name
        # If no player can move - the game ends in a tie
        else:
            if p1_movements == p2_movements == 0:
                return "Tie"
        # The game does not end
        return None