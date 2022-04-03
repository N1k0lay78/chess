from time import time

import pygame
import ctypes

from Source.settings import params
from core.UI.BaseUI import BaseUI


class InputField(BaseUI):
    def __init__(self, window, pos, placeholder, color, type, size=(10, 10), align_center=False):
        super().__init__(window, pos, un_active_on_mouse_up=False, size=size)
        self.placeholder = placeholder
        self.align_center = align_center
        self.color = color
        self.type = type

        # ready to action
        self.ready = False

        # settings
        self.u = ctypes.windll.LoadLibrary("user32.dll")
        self.time_to_zajim = 0.6
        self.delay_print = 0.02
        self.old_time = 0

        # for typing
        self.text = ""

        self.forbidden_symbols = ["`"]
        self.codes = [20, 26, 8, 21, 23, 28, 24, 12, 18, 19, 47, 48, 4, 22, 7, 9, 10, 11, 13, 14, 15, 51, 52, 29, 27, 6,
                      25, 5, 17, 16, 54, 55, 56, 53, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 45, 46, 225, 44, 42, 224,
                      40, 43, 226]  # 79, 80, 81, 82
        self.code_to_letter = {20: 'q', 26: 'w', 8: 'e', 21: 'r', 23: 't', 28: 'y', 24: 'u', 12: 'i', 18: 'o', 19: 'p',
                               47: '[', 48: ']', 4: 'a', 22: 's', 7: 'd', 9: 'f', 10: 'g', 11: 'h', 13: 'j', 14: 'k',
                               15: 'l', 51: ';', 52: "'", 29: 'z', 27: 'x', 6: 'c', 25: 'v', 5: 'b', 17: 'n', 16: 'm',
                               54: ',', 55: '.', 56: '/', 53: "`", 30: "1", 31: "2", 32: "3", 33: "4", 34: "5", 35: "6",
                               36: "7", 37: "8", 38: "9", 39: "0", 45: "-", 46: "=", 44: " ", 42: "bs"}
        self.code_to_special = {225: "sh", 44: "sp", 42: "bs", 224: "ct", 40: "en", 43: "tb", 226: "al"}
        self.rus = {'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
                    '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л',
                    'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
                    ',': 'б', '.': 'ю',
                    '`': 'ё'}
        self.special_symbols = {"1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*",
                                "9": "(", "0": ")", "-": "_", "=": "+", ";": ":", "'": '"', ",": "<", ".": ">",
                                "`": "~", "@": '"', "#": "№", "$": ";", "^": ":", "&": "?"}
        self.pressed_special = {'sh': False, 'sp': False, 'bs': False, 'ct': False, 'en': False, 'tb': False,
                                'al': False}
        self.pressed_letters = {}

    def draw(self, pos=(0, 0)):
        if self.text:
            render = self.window.game.render_text(self.text, self.color[0])
        else:
            render = self.window.game.render_text(self.placeholder, self.color[1])
        if self.align_center:
            pos = [pos[0] + self.pos[0] + (self.get_size()[0] - render.get_width()) // 2, pos[1] + self.pos[1]]
        else:
            pos = [pos[0] + self.pos[0], pos[1] + self.pos[1]]
        self.window.game.screen.blit(render, pos)

    def get_language(self):
        if hex(getattr(self.u, "GetKeyboardLayout")(0)) == '0x4190419':
            return True
        return False

    def update(self):
        cur_time = time()
        used = []
        delta = cur_time - self.old_time
        pressed_buttons = list(pygame.key.get_pressed())
        is_rus = self.get_language()
        for n_one in self.codes:
            if pressed_buttons[n_one]:
                if n_one in self.code_to_letter:
                    seal = self.code_to_letter[n_one]
                    if self.pressed_special["sh"] and seal in self.special_symbols:
                        seal = self.special_symbols[seal]
                        if is_rus and seal in self.special_symbols:
                            seal = self.special_symbols[seal]
                    elif is_rus and seal in self.rus:
                        seal = self.rus[seal]
                    if seal not in self.pressed_letters:
                        if seal not in self.forbidden_symbols:
                            self.pressed_letters[seal] = 0
                            if len(seal) == 1:
                                self.text += seal
                            else:
                                self.backspace()
                    else:
                        self.pressed_letters[seal] += delta
                        if self.pressed_letters[seal] > self.time_to_zajim:
                            if len(seal) == 1:
                                self.text += seal
                            else:
                                self.backspace()
                            self.pressed_letters[seal] -= self.delay_print
                    used.append(seal)
                if n_one in self.code_to_special:
                    self.pressed_special[self.code_to_special[n_one]] = True
                    used.append(self.code_to_special[n_one])
        for key in list(self.pressed_letters.keys()):
            if key not in used:
                self.pressed_letters.pop(key)
        for key in self.pressed_special.keys():
            if key not in used:
                self.pressed_special[key] = False
        self.old_time = cur_time
        if self.type == "code":
            self.code_checker()
        elif self.type == "nickname":
            self.nickname_check()
        else:
            self.text_checker()
        # print(self.pressed_letters)

    def code_checker(self):
        text = "".join(self.text.split())
        self.ready = text.isdigit() and len(text) == 4

        if self.ready:
            params["code"] = int(text)
        else:
            params["code"] = 0

        res = []
        for i in range(len(text)):
            if text[i].isdigit() and len(res) < 4:
                res.append(text[i])
        self.text = " ".join(res)

    def nickname_check(self):
        res = ""
        for char in self.text:
            if char in "qwertyuiopasdfghjklzxcvbnm_-1234567890" and len(res) < 15:
                res += char
        self.ready = len(res) > 7
        self.text = res

    def text_checker(self):
        if len(self.text) > 50:
            self.text = self.text[:50]

    def backspace(self):
        if len(self.text) > 0:
            if self.type == "code":
                if self.pressed_special["ct"]:
                    self.text = ""
                else:
                    self.text = " ".join(self.text.split()[:-1])
            elif self.type == "nickname":
                if self.pressed_special["ct"]:
                    self.text = "_".join(self.text.split('_')[:-1])
                else:
                    self.text = self.text[:-1]
            else:
                if self.pressed_special["ct"]:
                    self.text = self.text.rstrip()[:-len(self.text.split()[-1])].rstrip()
                else:
                    self.text = self.text[:-1]


# pygame.init()
# screen = pygame.display.set_mode((600, 600))
# pygame.display.set_caption("My Game")
# clock = pygame.time.Clock()
# inp = InputField(None, None, None, None)
# while True:
#     inp.update()
#     print(inp.text)
#     for event in pygame.event.get():
#         pass
#         if event.type == pygame.QUIT:
#             running = False
#     print(pygame.key.get_pressed().count(1))