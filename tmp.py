from random import choice

"""
for i in range(10000):
    n = bin(i)[2:]
    if i % 2 == 0:
        n += bin(n.count('1'))[2:]
    else:
        n += '00'
    if int(n, 2) > 55:
        print(i)
        break

for i in range(-1000, 1000):
    s = i
    n = 1
    while s < 50:
        s += 10
        n *= 8
    if n == 512:
        print(i)


def to_five(n, k):
    r = ""
    while n != 0:
        r = str(n % k) + r
        n //= k
    return r


# print(to_five(5))
# print(to_five(4))
# print(to_five(6))

c = 0
for i in range(4**5, 4**6-1):
    n = to_five(i, 4)
    if n.count('1') == 2 and n[-1] != '1':
        c += 1
print(c)

with open("stream.txt", 'r') as inp:
    with open("out.txt", 'w') as out:
        out.write(''.join([num for num in inp.readlines() if num.strip() != '' and num.strip()[-1] == '5']))

file = "input.txt"
res = 'output' + file[5:]


def logic(data) -> str:
    res = ""
    mn1 = "qwertyuiopasdfghjklzxcvbnm_"
    mn2 = mn1 + '1234567890'

    for elem in data[1:]:
        elem = elem.lower()
        if elem[0] in mn1 and all([char in mn2 for char in elem[1:]]):
            res += 'YES\n'
        else:
            res += 'NO\n'
    return res


def logic(data) -> str:
    res = ""
    mn1 = "qeyuioaj"
    for elem in data[0]:
        if elem not in mn1:
            res += elem
    return res


def logic(data) -> str:
    text = data[0].lower()
    text = text.split('.')[0]
    mn1 = "qwertyuiopasdfghjklzxcvbnm"
    sl = {}
    for elem in text:
        if elem in mn1:
            if elem not in sl:
                sl[elem] = 1
            else:
                sl[elem] += 1
    max_n, max_k = 0, ''
    for key, val in sl.items():
        if (val == max_n and ord(max_k) > ord(key)) or val > max_n:
            max_k = key
            max_n = val
    return f'{max_k} {max_n}'


def logic(data) -> str:
    num = '0'
    res = 0
    for elem in data[0]:
        if elem.isdigit():
            num += elem
        else:
            res += int(num)
            num = '0'
    return str(res)


def logic(data) -> str:
    return str(max([int(num) for num in data if num != '']))


file1 = "input.txt"
output = "output" + file1[5:]

with open(file1, 'r') as inp:
    data = list(map(lambda s: s.strip(), inp.readlines()))

with open(output, 'w') as out:
    out.write(logic(data))
"""
