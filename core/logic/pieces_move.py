def elephant_move(self, pos):
    move_x, move_y = pos[0] - self.cell[0], pos[1] - self.cell[1]
    # check that we are moving diagonally
    if move_y != 0 and move_x / move_y in (-1, 1):
        # get direction
        move_x = 1 if move_x > 0 else -1
        move_y = 1 if move_y > 0 else -1
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return all([self.check_clear_cell((self.cell[0] + move_x * i, self.cell[1] + move_y * i)) for i in range(1, abs(self.cell[0] - pos[0]))]) and self.check_not_friendly_cell(pos)
    return False


def horse_move(self, pos):
    # clockwise from 12 o'clock
    moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
    # heck that the target is where we can move
    return any([True for move in moves if pos == (self.cell[0] + move[0], self.cell[1] + move[1]) and self.check_not_friendly_cell(pos)])


def king_move(self, pos):
    # check that we are moving one cell
    if abs(self.cell[0] - pos[0]) < 2 and abs(self.cell[1] - pos[1]) < 2:
        return self.check_not_friendly_cell(pos)
    # castling check
    figure = self.get_piece(pos)
    if self.is_can and figure.name == "R" and not figure.is_can and figure.color == self.color:
        figure.set_cell(self.cell[:])
        return True
    return False


def logic_pawn_move(self, pos):
    if pos[0] == self.cell[0]:
        # check that the point is 1 cell forward
        if pos[1] == self.cell[1] - (1 if self.color % 2 == 0 else -1) and self.check_clear_cell(pos):
            return True
        # if this is the first move, then we can move 2 cells
        elif self.is_can and pos[1] == self.cell[1] - (2 if self.color % 2 == 0 else -2) and \
                self.check_clear_cell(pos):
            return True
    # if they want to go sideways, then we check that we can go and that there is an enemy
    elif (pos[0] + 1 == self.cell[0] or pos[0] - 1 == self.cell[0]) and \
            pos[1] == self.cell[1] - (1 if self.color % 2 == 0 else -1) and self.check_eat(pos):
        return True
    return False


def game_pawn_move(self, pos):
    if pos[0] == self.cell[0]:
        # check that the point is 1 cell forward
        if pos[1] == self.cell[1] - 1 and self.check_clear_cell(pos):
            return True
        # if this is the first move, then we can move 2 cells
        elif self.is_can and pos[1] == self.cell[1] - 2 and self.check_clear_cell(pos):
            return True
    # if they want to go sideways, then we check that we can go and that there is an enemy
    elif (pos[0] + 1 == self.cell[0] or pos[0] - 1 == self.cell[0]) and \
            pos[1] == self.cell[1] - 1 and self.check_eat(pos):
        return True
    return False


def queen_move(self, pos):
    move_x, move_y = pos[0] - self.cell[0], pos[1] - self.cell[1]
    # check that we are moving diagonally, or vertically, or horizontally
    if (move_x != move_y and (move_x == 0 or move_y == 0)) or (move_y != 0 and move_x / move_y in (-1, 1)):
        # get direction
        move_x = 1 if move_x > 0 else (-1 if move_x < 0 else 0)
        move_y = 1 if move_y > 0 else (-1 if move_y < 0 else 0)
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return all([self.check_clear_cell((self.cell[0] + move_x * i, self.cell[1] + move_y * i)) for i in range(1, abs(self.cell[0] - pos[0] if move_x else self.cell[1] - pos[1]))]) and self.check_not_friendly_cell(pos)
    return False


def rook_move(self, pos):
    move_x, move_y = pos[0] - self.cell[0], pos[1] - self.cell[1]
    # check that we are moving vertically or horizontally
    if move_x != move_y and (move_x == 0 or move_y == 0):
        # get direction
        move_x = 1 if move_x > 0 else (-1 if move_x < 0 else 0)
        move_y = 1 if move_y > 0 else (-1 if move_y < 0 else 0)
        # make ray cast to the target, if it did not intersect with anything, then we go to the cell
        # we check that there is either nothing with the destination or the enemy
        return all([self.check_clear_cell((self.cell[0] + move_x * i, self.cell[1] + move_y * i)) for i in range(1, abs(self.cell[0] - pos[0] + self.cell[1] - pos[1]))]) and self.check_not_friendly_cell(pos)
    return False
