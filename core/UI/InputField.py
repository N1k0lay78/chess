from time import time
from BaseUI import BaseUI
import pygame
import ctypes


class InputField(BaseUI):
    def __init__(self, window, pos, placeholder, color):
        super().__init__(window, pos)
        self.placeholder = placeholder
        self.color = color

        # settings
        self.u = ctypes.windll.LoadLibrary("user32.dll")
        self.time_to_zajim = 0.7
        self.delay_print = 0.025
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
                        if is_rus:
                            seal = self.special_symbols[seal]
                    elif is_rus and seal in self.rus:
                        seal = self.rus[seal]
                    if seal not in self.pressed_letters:
                        if seal not in self.forbidden_symbols:
                            self.pressed_letters[seal] = 0
                            if len(seal) == 1:
                                self.text += seal
                            else:
                                self.text = self.text[:-1]
                    else:
                        self.pressed_letters[seal] += delta
                        if self.pressed_letters[seal] > self.time_to_zajim:
                            if len(seal) == 1:
                                self.text += seal
                            else:
                                self.text = self.text[:-1]
                            self.pressed_letters[seal] -= self.delay_print
                    used.append(seal)
                if n_one in self.code_to_special:
                    self.pressed_special[self.code_to_special[n_one]] = True
                    used.append(self.code_to_special[n_one])
        for key in list(self.pressed_letters.keys()):
            if key not in used:
                self.pressed_letters.pop(key)
                print("DELETE")
        for key in self.pressed_special.keys():
            if key not in used:
                self.pressed_special[key] = False
        self.old_time = cur_time
        # print(self.pressed_letters)


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