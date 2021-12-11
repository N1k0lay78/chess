from core.textures.load_image import load_image


class TileSet:
    def __init__(self, filename, grid_size):
        self.image = load_image(filename)
        self.grid_size = grid_size
        self.max_x = self.image.get_size()[0]//self.grid_size[0]
        self.max_y = self.image.get_size()[1]//self.grid_size[1]
        self.max_index = self.max_y * self.max_x

    def __getitem__(self, item):
        if type(item) is int:
            if 0 <= item < self.max_index:
                item = (item % self.max_x, item // self.max_x)
            else:
                raise Exception(f"index {item} out of tile set")
        elif type(item) is tuple:
            if not (0 <= item[0] < self.max_x and 0 <= item[1] < self.max_y):
                raise Exception(f"index {item} out of tile set")
        return self.image.subsurface(item[0] * self.grid_size[0], item[1] * self.grid_size[1], *self.grid_size)
