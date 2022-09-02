import select
import socket
import queue
from test_server.commands import commands_lobby, commands_game, commands_official, commands_social, commands_ui

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)  # Неблокирующийся сокет
server.bind(("127.0.0.1", 1080))
server.listen()

sockets = [server]
message_queues = {}

clients = {}
new_clients = []
messages = {}
nicknames = []


def close_connection(con):
    peer = con.getpeername()
    if peer in clients:
        del clients[peer]
    sockets.remove(con)
    if con in message_queues:
        del message_queues[con]
    con.close()


# gethostname()
# gethostbyname()
# gethostbyaddr()

# Пока есть хоть один сокет
while sockets:
    # Опрашиваем сокеты на готовность к чтению, записи, ошибки.
    # С таймаутом в 1 секунду для того, чтобы программа реагировала
    # на другие события.
    readable, writable, exceptional = select.select(sockets, sockets, sockets, 1)

    while len(new_clients):
        peername, conn = new_clients.pop(0), None

        if peername in clients:
            continue

        for wr in writable:
            if wr.getpeername() == peername:
                conn = wr
                break

        if not conn:
            continue

        try:
            conn.send(bytes("suco", encoding="utf-8"))
            clients[peername] = [conn, None, None, []]
            messages[peername] = []
            print(clients)
        except Exception as e:
            print(e)

    for s in readable:  # Для каждого сокета готового к чтению
        if s is server:  # Если это сокет принимающий соединения
            connection, client_address = s.accept()
            connection.setblocking(0)  # Этот клиентский сокет тоже будет неблокируемым
            sockets.append(connection)  # Добавляем клиентский сокет в список сокетов
            message_queues[connection] = queue.Queue()  # Создаём очередь сообщений для сокета
            # print(help(connection))
            print(connection.getpeername())
            # print(connection.)
            new_clients.append(connection.getpeername())
        else:
            data = None
            try:
                if s in clients:
                    data = s.recv(1024).decode()  # Читаем без блокировки
                    messages[s.getpeername()].append(data)
                    # print(data)
                    # for sock in writable:
                        # print(type(sock))
                        # sock.send(bytes("Не надо мне ничего присылать", encoding="utf-8"))
            except:
                close_connection(s)  # В случае ошибки закрываем этот сокет и удаляем
            else:  # Если ошибка не произошла
                if data:  # И данные получены
                    for c in message_queues:  # Обходим все очереди сообщений
                        if c != s:  # Кроме очереди текущего сокета
                            message_queues[c].put(data)  # Отправляем данные в каждую очередь
                else:
                    # Если данных нет в сокете готовом для чтения
                    # значит он в состоянии закрытия на клиентской
                    # стороне. Закрываем его на стороне сервера.
                    close_connection(s)

    for s in writable:  # Для каждого сокета готового к записи
        try:
            next_msg = message_queues[s].get_nowait()  # Получаем сообщение из очереди
        except queue.Empty:
            pass  # Игнорируем пустые очереди
        except KeyError:
            pass  # Игнорируем очереди удалённые до того, как до них дошла очередь обработки
        else:
            s.send(next_msg)  # Отправляем без блокировки

    for s in exceptional:  # Для каждого сбойного сокета
        close_connection(s)  # Закрываем сбойный сокет


"""
Задачи:
1 - Решить, как обрабатывать сообщения от юзеров
- Если обработка сообщения в силах сервера (команда находится в группах: official, social (ui?)), то мы обрабатываем его
на сервере, вызывая специальную функцию раз в тик, обрабатывающую все по 2 команды от юзеров в тик, при этом надо 
поставить ограничения но кол-во входящих сообщений от пользователя, вплоть до временной заморозки приёма сообщений от
пользователя на некоторое время (до 5 секунд). Если это не помогло - то на 15. Если и это не остановило строптивого, то
на удаляем его, ибо заебал. Во время временного бана посылаем юзеру сообщение о бане. Временно блокируем ему экран в
игре, показывая окошко с таймером и объяснением, что больше делать не надо. Для обработки сообщений должна быть функция,
вызывающая функции посредники с кодом (диверсифицировать нагрузку)

2 - Решить, как отправлять сообщения пользователям
Создаём список у пользователя со сообщениями, которые надо отправить. Отправляем по 1 сообщения за тик, не более.

3 - Решить, как спрашивать nickname у пользователя. Обязательный аттрибут
- Занести пользователя в спец список и послать команду о подключении. Далее в течении определённого времени ожидать 
сообщение с новым никнеймом и не принимать другие. Если в течении определённого времени не пришёл никнейм, то мы удаляем
пользователя. Если никнейм пришёл, то проверить его уникальность. Никнейм не уникален? Посылаем запрос на новый никнейм,
отключаем человека и повторяем сценарий

4 - Сделать шифровку/обмен ключами шифра
- Посылать ключ при передаче никнейма и утверждении его уникальности. Для упрощения создать список с занятыми 
никнеймами + производить его чистку/увеличение

5 - Сделать переадресацию сообщений
- Сделать вызов функции у сервера, если сообщение в его юрисдикции, то сервер его обработает, иначе добавлять к 
пользователю в специальный список (при подключении юзера к лобби/игре). Из этого списка сообщения берёт комната/лобби и
работает с ним в штатном режиме
"""