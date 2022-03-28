import pygame
import ctypes
from BaseUI import BaseUI


class InputField(BaseUI):
    def __init__(self, window, pos, placeholder, color):
        super().__init__(window, pos)
        self.placeholder = placeholder
        self.color = color
        self.text = ""
        self.push_time = 1000
        self.pushed_buttons = 0

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            print(event.type)
        elif event.type == pygame.KEYUP:
            pass


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

code_to_letter = {20: 'q', 26: 'w', 8: 'e', 21: 'r', 23: 't', 28: 'y', 24: 'u', 12: 'i', 18: 'o', 19: 'p', 47: '[',
                  48: ']', 4: 'a', 22: 's', 7: 'd', 9: 'f', 10: 'g', 11: 'h', 13: 'j', 14: 'k', 15: 'l', 51: ';',
                  52: "'", 29: 'z', 27: 'x', 6: 'c', 25: 'v', 5: 'b', 17: 'n', 16: 'm', 54: ',', 55: '.', 56: '/',
                  53: "`", 30: "1", 31: "2", 32: "3", 33: "4", 34: "5", 35: "6", 36: "7", 37: "8", 38: "9", 39: "0",
                  225: "sh", 44: "sp", 42: "bs", 224: "ct", 40: "en", 43: "tb", 226: "al", 79: "ri", 80: "le",
                  81: "do", 82: "up"}

letter_to_code = {20: 'q', 26: 'w', 8: 'e', 21: 'r', 23: 't', 28: 'y', 24: 'u', 12: 'i', 18: 'o', 19: 'p', 47: '[',
                  48: ']', 4: 'a', 22: 's', 7: 'd', 9: 'f', 10: 'g', 11: 'h', 13: 'j', 14: 'k', 15: 'l', 51: ';',
                  52: "'", 29: 'z', 27: 'x', 6: 'c', 25: 'v', 5: 'b', 17: 'n', 16: 'm', 54: ',', 55: '.', 56: '/',
                  53: '`', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0',
                  225: 'sh', 44: 'sp', 42: 'bs', 224: 'ct', 40: 'en', 43: 'tb', 226: 'al', 79: 'ri', 80: 'le',
                  81: 'do', 82: 'up'}


def capslock():
    import ctypes
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return ((hllDll.GetKeyState(VK_CAPITAL)) & 0xffff) != 0


running = True
while running:
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            mouse_buttons = list(pygame.key.get_pressed())
            # print(code_to_letter[list(pygame.key.get_pressed()).index(1)])
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
