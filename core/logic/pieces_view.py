def big_view(self, cell):
    return self.cell[0] - 2 <= cell[0] <= self.cell[0] + 2 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1


def small_view(self, cell):
    return self.cell[0] - 1 <= cell[0] <= self.cell[0] + 1 and self.cell[1] - 1 <= cell[1] <= self.cell[1] + 1
