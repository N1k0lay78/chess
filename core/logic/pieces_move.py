def elephant_path(self, pos):
    move_x, move_y = pos[0] - self.c, pos[1] - self.r
    # check that we are moving diagonally
    if move_y != 0 and move_x / move_y in (-1, 1):
        # get direction
        move_x = 1 if move_x > 0 else -1
        move_y = 1 if move_y > 0 else -1
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return [(self.c + move_x * i, self.r + move_y * i, 0)
                for i in range(1, abs(self.c - pos[0]))] + [(*pos, 1)]


def elephant_move(self, pos):
    move_x, move_y = pos[0] - self.c, pos[1] - self.r
    # check that we are moving diagonally
    if move_y != 0 and move_x / move_y in (-1, 1):
        # get direction
        move_x = 1 if move_x > 0 else -1
        move_y = 1 if move_y > 0 else -1
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return all([self.check_clear_cell((self.c + move_x * i, self.r + move_y * i))
                    for i in range(1, abs(self.c - pos[0]))]) and self.check_not_friendly_cell(pos)
    return False


def horse_path(self, pos):
    # clockwise from 12 o'clock
    moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
    # heck that the target is where we can move
    for move in moves:
        if pos[0] == self.c + move[0] and pos[1] == self.r + move[1]:
            return [(*pos, 1)]


def horse_move(self, pos):
    # clockwise from 12 o'clock
    moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
    # heck that the target is where we can move
    return any([True for move in moves
                if pos[0] == self.c + move[0] and pos[1] == self.r + move[1]
                and self.check_not_friendly_cell(pos)])


def king_path(self, pos):
    # check that we are moving one cell
    if abs(self.c - pos[0]) < 2 and abs(self.r - pos[1]) < 2:
        return [(*pos, 1)]

    if self.i and abs(self.c - pos[0]) == 2 and self.r - pos[1] == 0:
        if self.c - pos[0] > 0:
            return [(1, self.r, 0), (2, self.r, 0), (3, self.r, 0)]
        else:
            return [(5, self.r, 0), (6, self.r, 0)]
    # castling check
    # figure = self.get_piece(pos)
    # if figure and self.i and figure.t == "R" and figure.i and figure.s == self.s:
    #     return  # self.check_castling(figure, pos)


def king_move(self, pos):
    # check that we are moving one cell
    if abs(self.c - pos[0]) < 2 and abs(self.r - pos[1]) < 2 and self.check_not_friendly_cell(pos):
        return True
    # castling check
    figure = self.get_piece(pos)
    if figure and self.i and figure.t == "R" and figure.i and figure.s == self.s:
        return self.check_castling(figure, pos)
    return False


def logic_pawn_path(self, pos):
    if pos[0] == self.c:
        # check that the point is 1 cell forward
        if pos[1] == self.r - (1 if self.s % 2 == 0 else -1):
            return [(*pos, 0)]
        # if this is the first move, then we can move 2 cells
        elif self.i and pos[1] == self.r - (2 if self.s % 2 == 0 else -2):
            return [(self.c, self.r - (1 if self.s % 2 == 0 else -1), 0), (*pos, 0)]
    # if they want to go sideways, then we check that we can go and that there is an enemy
    elif (pos[0] + 1 == self.c or pos[0] - 1 == self.c) and \
            pos[1] == self.r - (1 if self.s % 2 == 0 else -1):
        return [(*pos, 2)]


def game_pawn_move(self, pos):
    if pos[0] == self.c:
        # check that the point is 1 cell forward
        if pos[1] == self.r - 1 and self.check_clear_cell(pos):
            return True
        # if this is the first move, then we can move 2 cells
        elif self.i and pos[1] == self.r - 2 and self.check_clear_cell(pos)\
                and self.check_clear_cell((self.c, self.r - 1)):
            return True
    # if they want to go sideways, then we check that we can go and that there is an enemy
    elif (pos[0] + 1 == self.c or pos[0] - 1 == self.c) and \
            pos[1] == self.r - 1 and self.check_eat(pos):
        return True
    return False


def queen_path(self, pos):
    move_x, move_y = pos[0] - self.c, pos[1] - self.r
    # check that we are moving diagonally, or vertically, or horizontally
    if (move_x != move_y and (move_x == 0 or move_y == 0)) or (move_y != 0 and move_x / move_y in (-1, 1)):
        # get direction
        move_x = 1 if move_x > 0 else (-1 if move_x < 0 else 0)
        move_y = 1 if move_y > 0 else (-1 if move_y < 0 else 0)
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return [(self.c + move_x * i, self.r + move_y * i, 0)
                for i in range(1, abs(self.c - pos[0] if move_x else self.r - pos[1]))] + [(*pos, 1)]
    return False


def queen_move(self, pos):
    move_x, move_y = pos[0] - self.c, pos[1] - self.r
    # check that we are moving diagonally, or vertically, or horizontally
    if (move_x != move_y and (move_x == 0 or move_y == 0)) or (move_y != 0 and move_x / move_y in (-1, 1)):
        # get direction
        move_x = 1 if move_x > 0 else (-1 if move_x < 0 else 0)
        move_y = 1 if move_y > 0 else (-1 if move_y < 0 else 0)
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return all([self.check_clear_cell((self.c + move_x * i, self.r + move_y * i))
                    for i in range(1, abs(self.c - pos[0] if move_x else self.r - pos[1]))]) and self.check_not_friendly_cell(pos)
    return False


def rook_path(self, pos):
    move_x, move_y = pos[0] - self.c, pos[1] - self.r
    # check that we are moving vertically or horizontally
    if move_x != move_y and (move_x == 0 or move_y == 0):
        # get direction
        move_x = 1 if move_x > 0 else (-1 if move_x < 0 else 0)
        move_y = 1 if move_y > 0 else (-1 if move_y < 0 else 0)
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return [(self.c + move_x * i, self.r + move_y * i, 0)
                for i in range(1, abs(self.c - pos[0] + self.r - pos[1]))] + [(*pos, 1)]


def rook_move(self, pos):
    move_x, move_y = pos[0] - self.c, pos[1] - self.r
    # check that we are moving vertically or horizontally
    if move_x != move_y and (move_x == 0 or move_y == 0):
        # get direction
        move_x = 1 if move_x > 0 else (-1 if move_x < 0 else 0)
        move_y = 1 if move_y > 0 else (-1 if move_y < 0 else 0)
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return all([self.check_clear_cell((self.c + move_x * i, self.r + move_y * i))
                    for i in range(1, abs(self.c - pos[0] + self.r - pos[1]))]) and self.check_not_friendly_cell(pos)
    return False
