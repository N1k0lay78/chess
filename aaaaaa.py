import pygame
import ctypes

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

u = ctypes.windll.LoadLibrary("user32.dll")
pf = getattr(u, "GetKeyboardLayout")

let = list("qwertyuiop[]asdfghjkl;'zxcvbnm,./")
ind = 0
dc_l = {}
l_dc = {}
forbidden_symbols = {"`": "'"}

code_to_letter = {20: 'q', 26: 'w', 8: 'e', 21: 'r', 23: 't', 28: 'y', 24: 'u', 12: 'i', 18: 'o', 19: 'p', 47: '[',
                  48: ']', 4: 'a', 22: 's', 7: 'd', 9: 'f', 10: 'g', 11: 'h', 13: 'j', 14: 'k', 15: 'l', 51: ';',
                  52: "'", 29: 'z', 27: 'x', 6: 'c', 25: 'v', 5: 'b', 17: 'n', 16: 'm', 54: ',', 55: '.', 56: '/',
                  53: "`", 30: "1", 31: "2", 32: "3", 33: "4", 34: "5", 35: "6", 36: "7", 37: "8", 38: "9", 39: "0",
                  45: "-", 46: "=", 225: "sh", 44: "sp", 42: "bs", 224: "ct", 40: "en", 43: "tb", 226: "al", 79: "rig",
                  80: "lef", 81: "dow", 82: "upp"}

letter_to_code = {'q': 20, 'w': 26, 'e': 8, 'r': 21, 't': 23, 'y': 28, 'u': 24, 'i': 12, 'o': 18, 'p': 19, '[': 47,
                  ']': 48, 'a': 4, 's': 22, 'd': 7, 'f': 9, 'g': 10, 'h': 11, 'j': 13, 'k': 14, 'l': 15, ';': 51,
                  "'": 52, 'z': 29, 'x': 27, 'c': 6, 'v': 25, 'b': 5, 'n': 17, 'm': 16, ',': 54, '.': 55, '/': 56,
                  '`': 53, '1': 30, '2': 31, '3': 32, '4': 33, '5': 34, '6': 35, '7': 36, '8': 37, '9': 38, '0': 39,
                  "-": 45, "=": 46, 'sh': 225, 'sp': 44, 'bs': 42, 'ct': 224, 'en': 40, 'tb': 43, 'al': 226, 'rig': 79,
                  'lef': 80, 'dow': 81, 'upp': 82}

special_symbols_en = {"1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(", "0": ")", "-": "_", "=": "+", ";": ":", "'": '"', ",": "<", ".": ">", "`": "~"}
special_symbols_ru = {"2": '"', "3": "№", "4": ";", "6": ":", "7": "?"}

pressed_letters = {}

running = True

while running:
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            mouse_buttons = list(pygame.key.get_pressed())
            # print(code_to_letter[list(pygame.key.get_pressed()).index(1)])
            print(list(pygame.key.get_pressed()).index(1))

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
    for n_one in code_to_letter.keys():
        if pressed_buttons[n_one]:
            print(code_to_letter[n_one])
