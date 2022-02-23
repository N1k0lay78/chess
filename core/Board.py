import pygame

from Source.settings import debug
from core.logic.PiecesManager import PiecesManager, game_pieces_dict, LoadingBoardError
from core.textures.Tileset import TileSet
from core.textures.load_image import load_image


class Board:
    def __init__(self, game, pos, size, color):
        # logic
        self.color = color
        self.game = game
        self.position = pos
        self.size = size
        self.board = []
        self.pause = False
        self.pieces_manager = PiecesManager(self.game, game_pieces_dict)
        self.step = 0
        # control
        self.focused = None
        self.dragging = False
        self.set_on_next = False
        self.last_mouse_pos = (0, 0)
        # surfaces
        self.pieces_tile_set = TileSet('pieces', (50, 150))
        self.surface = pygame.image.load('Source/Image/board.png')

    def draw(self):
        # draw the background
        self.game.screen.blit(self.surface, self.position)
        # draw the figures
        layers = {}
        for piece in self.board:
            if self.focused == piece and self.dragging:
                layers[100000] = [piece]
            if piece.pos[1] in layers:
                layers[piece.pos[1]].append(piece)
            else:
                layers[piece.pos[1]] = [piece]
        for key in sorted(list(layers.keys())):
            for figure in layers[key]:
                figure.draw()
        if self.focused and debug:
            pygame.draw.circle(self.game.screen, (255, 255, 255), (self.focused.pos[0] + 25,
                                                                   self.focused.pos[1]+35), 5)

    def update(self, event):
        # focused - the figure we are moving
        # dragging - whether to move the shape when moving the mouse
        if not self.pause:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.last_mouse_pos = event.pos
                figure = self.get_pos(((event.pos[0] - self.position[0]) // self.size[0],
                                       (event.pos[1] - self.position[1]) // self.size[1]))
                # is there a piece and check that its move
                if figure != None and figure.color == self.color == self.step % 2:
                    self.focused = figure
                    self.dragging = True
                elif figure is None:
                    self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                # move figure if dragging
                if self.dragging and self.focused:
                    self.focused.move((self.last_mouse_pos[0] - event.pos[0],
                                       self.last_mouse_pos[1] - event.pos[1]))
                    self.last_mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
                # move figure to new cell
                if self.focused:
                    self.focused.update(((self.focused.pos[0] + 25 - self.position[0]) // self.size[0],
                                         (self.focused.pos[1] + 35 - self.position[1]) // self.size[1]))

    def get_pos(self, pos):  # get a figure using position
        for i in range(len(self.board)):
            if self.board[i].cell[0] == pos[0] and self.board[i].cell[1] == pos[1]:
                return self.board[i]

    def remove_from_board(self, piece):
        # if the king died, then we recreate the game
        # if type(piece) == King:
        #     print(f"win is {'red' if piece.color == 0 else 'green'}")
        #     self.generate_board()
        # elif piece in self.board:
        self.board.remove(piece)

    def go_to_next_step(self):
        # self.step += 1
        # flip the board
        self.game.fog.update()

    def set_color(self, color):
        self.color = color

    def add_piece(self, code):
        try:
            self.board.append(self.pieces_manager.add_piece(code))
        except LoadingBoardError as e:
            print(e)

    def load_board(self, line):  # loading pieces from line with pieces info
        try:
            self.board = self.pieces_manager.read_line(line)
        except LoadingBoardError as e:
            self.board = []
            print(e)

    def set_pause(self, pause):
        self.pause = pause
