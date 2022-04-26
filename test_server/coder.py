from random import randint, choice
max_num = 4
let_big = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
let_small = "abcdefghijklmnopqrstuvwxyz"
all_lets = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
eng_big_let_inds = [65, 90]
eng_small_let_inds = [97, 122]
rus_big_let_inds = [1040, 1071]
rus_small_let_inds = [1072, 1103]
dict_of_ind = {
    True:
        {
            True: eng_big_let_inds,
            False: eng_small_let_inds
        },
    False:
        {
            True: rus_big_let_inds,
            False: rus_small_let_inds
        }
}


def ogranichitel(minmax, num):
    return minmax[0] + (num - minmax[0]) % (minmax[1] - minmax[0] + 1)


def gen_code(length):
    code = ""
    while len(code) < length:
        code += "".join([choice(all_lets) for i in range(randint(2, 9))])
        code += str(randint(0, max_num))
    return code[:length]


def coding(code, message):
    new_message = ""
    dop_z = 0
    dop_for_l = 0
    len_code = len(code) - 1
    for ind, elem in enumerate(message):
        while True:
            code_elem = code[ogranichitel([0, len_code], ind + dop_z)]
            # print(code_elem)
            if code_elem.isdigit():
                dop_z += 1 + int(code_elem)
                dop_for_l = int(code_elem) * (-1 if (dop_z + ind) % 2 else 1)
            else:
                break
        if elem.isalpha():
            is_big = code_elem.isupper()
            let_ind = 1 + (let_big.index(code_elem) if is_big else let_small.index(code_elem))
            new_message += chr(ogranichitel(dict_of_ind[elem in all_lets][elem.isupper()], ord(elem) + (let_ind + dop_for_l if ind % 2 and is_big or not (is_big or ind % 2) else -let_ind + dop_for_l)))
        elif elem.isdigit():
            is_big = code_elem.isupper()
            let_ind = 1 + (let_big.index(code_elem) if is_big else let_small.index(code_elem))
            new_message += str(ogranichitel([0, 9], int(elem) + (let_ind + dop_for_l if ind % 2 and is_big or not (is_big or ind % 2) else -let_ind + dop_for_l)))
        else:
            new_message += elem
    return new_message


def decoding(code, message):
    new_message = ""
    dop_z = 0
    dop_for_l = 0
    len_code = len(code) - 1
    for ind, elem in enumerate(message):
        while True:
            code_elem = code[ogranichitel([0, len_code], ind + dop_z)]
            # print(code_elem)
            if code_elem.isdigit():
                dop_z += 1 + int(code_elem)
                dop_for_l = int(code_elem) * (-1 if (dop_z + ind) % 2 else 1)
            else:
                break
        if elem.isalpha():
            is_big = code_elem.isupper()
            let_ind = 1 + (let_big.index(code_elem) if is_big else let_small.index(code_elem))
            new_message += chr(ogranichitel(dict_of_ind[elem in all_lets][elem.isupper()], ord(elem) - (let_ind + dop_for_l if ind % 2 and is_big or not (is_big or ind % 2) else -let_ind + dop_for_l)))
        elif elem.isdigit():
            is_big = code_elem.isupper()
            let_ind = 1 + (let_big.index(code_elem) if is_big else let_small.index(code_elem))
            new_message += str(ogranichitel([0, 9], int(elem) - (let_ind + dop_for_l if ind % 2 and is_big or not (is_big or ind % 2) else -let_ind + dop_for_l)))
        else:
            new_message += elem
    return new_message



# print(ord("a"))
# code = gen_code(100)
# fraze = "Пока кто-то сидит на вождении, я сижу дома, да прогаю. Кстати, в коде, который шифровальный, было 100 символов"
# co = coding(code, fraze)
# deco = decoding(code, co)
# print(code)
# print(co)
# print(deco)
# print(deco == fraze)
# # code = gen_code(100)
# print(code)
# while True:
#     input(randint(2, 9))
# print(randint(0, max_num))
