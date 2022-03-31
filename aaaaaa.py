import pygame
import ctypes
from time import time

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

u = ctypes.windll.LoadLibrary("user32.dll")

forbidden_symbols = ["`"]

codes = [20, 26, 8, 21, 23, 28, 24, 12, 18, 19, 47, 48, 4, 22, 7, 9, 10, 11, 13, 14, 15, 51, 52, 29, 27, 6, 25, 5, 17,
         16, 54, 55, 56, 53, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 45, 46, 225, 44, 42, 224, 40, 43, 226] # 79, 80, 81, 82

code_to_letter = {20: 'q', 26: 'w', 8: 'e', 21: 'r', 23: 't', 28: 'y', 24: 'u', 12: 'i', 18: 'o', 19: 'p', 47: '[',
                  48: ']', 4: 'a', 22: 's', 7: 'd', 9: 'f', 10: 'g', 11: 'h', 13: 'j', 14: 'k', 15: 'l', 51: ';',
                  52: "'", 29: 'z', 27: 'x', 6: 'c', 25: 'v', 5: 'b', 17: 'n', 16: 'm', 54: ',', 55: '.', 56: '/',
                  53: "`", 30: "1", 31: "2", 32: "3", 33: "4", 34: "5", 35: "6", 36: "7", 37: "8", 38: "9", 39: "0",
                  45: "-", 46: "=", 44: " ", 42: "bs"}  # 79: "rig", 80: "lef", 81: "dow", 82: "upp"

code_to_special = {225: "sh", 44: "sp", 42: "bs", 224: "ct", 40: "en", 43: "tb", 226: "al"}

rus = {'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х',
       ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж',
       "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '`': 'ё'}

special_symbols = {"1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(",
                   "0": ")", "-": "_", "=": "+", ";": ":", "'": '"', ",": "<", ".": ">", "`": "~", "@": '"',
                   "#": "№", "$": ";", "^": ":", "&": "?"}

pressed_letters = {}

pressed_special = {'sh': False, 'sp': False, 'bs': False, 'ct': False, 'en': False, 'tb': False, 'al': False}

time_to_zajim = 0.7
delay_print = 0.025
running = True
old_time = time()
text = ""


def get_language():
    pf = getattr(u, "GetKeyboardLayout")
    if hex(pf(0)) == '0x4190419':
        return True
    return False


lv = ""
while running:
    cur_time = time()
    used = []
    delta = cur_time - old_time
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
            # pass
            # mouse_buttons = list(pygame.key.get_pressed())
            # print(code_to_letter[list(pygame.key.get_pressed()).index(1)])
            # print(list(pygame.key.get_pressed()).index(1))

            # print(event.type, type(event.type/), str(event.type))
            # print(list(pygame.key.get_pressed()))
            # print(event.keycode)
            # print(pygame.key.start_text_input())

            # print(list(pygame.key.get_pressed()).index(1))
            # dc_l[list(pygame.key.get_pressed()).index(1)] = let[ind]
            # l_dc[let[ind]] = list(pygame.key.get_pressed()).index(1)
            # ind += 1
            # print(event.key)

    pressed_buttons = list(pygame.key.get_pressed())
    is_rus = get_language()
    for n_one in codes:
        if pressed_buttons[n_one]:
            if n_one in code_to_letter:
                seal = code_to_letter[n_one]
                if pressed_special["sh"] and seal in special_symbols:
                    seal = special_symbols[seal]
                    if is_rus:
                        seal = special_symbols[seal]
                elif is_rus and seal in rus:
                    seal = rus[seal]
                if seal not in pressed_letters:
                    if seal not in forbidden_symbols:
                        pressed_letters[seal] = 0
                        if len(seal) == 1:
                            text += seal
                        else:
                            text = text[:-1]
                else:
                    pressed_letters[seal] += delta
                    if pressed_letters[seal] > time_to_zajim:
                        if len(seal) == 1:
                            text += seal
                        else:
                            text = text[:-1]
                        pressed_letters[seal] -= delay_print
                used.append(seal)
            if n_one in code_to_special:
                pressed_special[code_to_special[n_one]] = True
                used.append(code_to_special[n_one])
    for key in list(pressed_letters.keys()):
        if key not in used:
            pressed_letters.pop(key)
    for key in pressed_special.keys():
        if key not in used:
            pressed_special[key] = False
    # print(pressed_letters)
    # print(pressed_special)
    if text != lv:
        print("\r" + text, end="")
    lv = text
    old_time = cur_time
