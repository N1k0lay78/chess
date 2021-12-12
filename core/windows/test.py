from Source.animations import test_button
from core.UI.BaseUI import BaseUI
from core.UI.Button import Button
from core.UI.PopUp import PopUp
from core.textures.Tileset import TileSet
from core.textures.load_image import load_image
from core.windows.Window import Window


class Test(Window):
    def __init__(self, screen):
        super().__init__(screen, max_fps=30)
        self.test = BaseUI(self, (100, 100), image=load_image('test'))
        self.test.add_child(BaseUI(self, (100, 100), image=load_image('test')))
        self.pop_up = PopUp(self, [300, 100], load_image('test_pop_up'))
        self.button = Button(self, (400, 100), TileSet('test_button', (100, 100)), test_button)

    def draw(self):
        self.screen.fill((20, 20, 50))
        self.test.draw()
        self.pop_up.draw()
        self.button.draw()

    def set_active(self, event):
        if self.test.check_collide_point(event.pos):
            self.set_active_object(self.test)
        elif self.pop_up.check_collide_point(event.pos):
            self.set_active_object(self.pop_up)
        elif self.button.check_collide_point(event.pos):
            self.set_active_object(self.button)

    def check_hover(self, event):
        self.test.check_collide_point(event.pos)
        self.pop_up.check_collide_point(event.pos)
        self.button.check_collide_point(event.pos)
