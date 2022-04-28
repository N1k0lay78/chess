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
messages = []


def close_connection(con):
    peer = con.getpeername()
    if peer in clients:
        del clients[peer]
    sockets.remove(con)
    if con in message_queues:
        del message_queues[con]
    con.close()


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
            clients[peername] = [conn, None]
            print(clients)
        except Exception as e:
            print(e)

    for s in readable:  # Для каждого сокета готового к чтению
        if s is server:  # Если это сокет принимающий соединения
            connection, client_address = s.accept()
            connection.setblocking(0)  # Этот клиентский сокет тоже будет неблокируемым
            sockets.append(connection)  # Добавляем клиентский сокет в список сокетов
            message_queues[connection] = queue.Queue()  # Создаём очередь сообщений для сокета
            new_clients.append(connection.getpeername())
        else:
            try:
                if s in clients:
                    data = s.recv(1024)  # Читаем без блокировки
                    messages.append([s.getpeername(), data])
                    print(data.decode())
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
