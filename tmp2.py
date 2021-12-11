from time import time, sleep

count = 10**4
rotate = ['—', '—', '—', '\\', '\\', '|', '|', '/', '/']
for i in range(count):
    print(f'\r{round((i+1)/count * 100, 2)}% \t{rotate[int(time()*4) % len(rotate)]} \tfile №{i}', end="")
    sleep(0.005)
