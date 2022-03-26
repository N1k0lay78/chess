from core.logic.PiecesManager import PiecesManager, game_pieces_dict, LoadingBoardError
from core.textures.Tileset import TileSet
from Source.special_functools import special_print
import pygame


class Board:
    def __init__(self, game, pos: tuple, size: tuple, color: int):
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
            for piece in layers[key]:
                piece.draw()
        if self.focused:  # Тут был дебаг, но фича заслуживает релиза
            pygame.draw.circle(self.game.screen, (255, 255, 255), (self.focused.pos[0] + 25,
                                                                   self.focused.pos[1] + 35), 5)

    def update(self, event):
        # focused - the piece we are moving
        # dragging - whether to move the shape when moving the mouse

        if self.pause:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.last_mouse_pos = event.pos
            piece = self.get_pos(((event.pos[0] - self.position[0]) // self.size[0],
                                  (event.pos[1] - self.position[1]) // self.size[1]))
            # is there a piece and check that its move
            if piece is not None and piece.color == self.color == self.step % 2:
                if self.focused:
                    self.focused.update([-1, -1])
                self.focused = piece
                self.dragging = True
            elif piece is None:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            # move piece if dragging
            if self.dragging and self.focused:
                self.focused.move((self.last_mouse_pos[0] - event.pos[0],
                                   self.last_mouse_pos[1] - event.pos[1]))
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # move piece to new cell
            if self.focused and self.dragging:
                self.dragging = False
                self.focused.update([(self.focused.pos[0] + 25 - self.position[0]) // self.size[0],
                                     (self.focused.pos[1] + 35 - self.position[1]) // self.size[1]])
            elif self.focused:
                self.focused.update([(event.pos[0] - self.position[0]) // self.size[0],
                                     (event.pos[1] - self.position[1]) // self.size[1]])

    def get_pos(self, pos):  # get a piece using position
        for i in range(len(self.board)):
            if self.board[i].cell[0] == pos[0] and self.board[i].cell[1] == pos[1]:
                return self.board[i]

    def remove_piece(self, piece):
        self.board.remove(piece)
        self.game.judge.on_remove(piece.name)

    def go_to_next_step(self):
        self.step += 1
        self.game.fog.update()

    def set_color(self, color):
        self.color = color

    def add_piece(self, code):
        try:
            self.board.append(self.pieces_manager.add_piece(code))
        except LoadingBoardError as e:
            special_print(e, level=10)

    def restart(self, line):
        self.step = 0
        self.color = 0
        self.focused = None
        self.load_board(line)

    def load_board(self, line):  # loading pieces from line with pieces info
        try:
            self.board = self.pieces_manager.read_line(line)
        except LoadingBoardError as e:
            self.board = []
            special_print(e, level=10)

    def set_pause(self, pause):
        self.pause = pause
