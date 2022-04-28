import select
import socket
import queue
from time import time


class Server():
    def __init__(self, ip, port):
        # Server
        self.server = None

        # Auxiliary vars
        self.sockets = [self.server]
        self.message_queues = {}
        self.clients = {}
        self.new_clients = []
        self.messages = {}
        self.used_nicknames = []
        self.wait_access = []

        self.ip = ip
        self.port = port

    def close_connection(self, con):
        peer = con.getpeername()
        if peer in self.clients:
            del self.clients[peer]
        self.sockets.remove(con)
        if con in self.message_queues:
            del self.message_queues[con]
        con.close()

    def main(self):
        while self.sockets:
            # Опрашиваем сокеты на готовность к чтению, записи, ошибки.
            # С таймаутом в 1 секунду для того, чтобы программа реагировала
            # на другие события.
            readable, writable, exceptional = select.select(self.sockets, self.sockets, self.sockets, 1)

            while len(self.new_clients):
                peername, conn = self.new_clients.pop(0), None

                if peername in self.clients:
                    continue

                for wr in writable:
                    if wr.getpeername() == peername:
                        conn = wr
                        break

                if not conn:
                    continue

                try:
                    conn.send(bytes("suco", encoding="utf-8"))
                    self.wait_access = [peername, time()]
                    self.clients[peername] = [conn, None, None, []]
                    self.messages[peername] = []  # ПЕРЕНЕСТИ СОЗДАНИЕ В ФУНКЦИЮ, ВЫЗЫВАЮЩУЮСЯ ПРИ ПОЛУЧЕНИИ НИКА
                    print(self.clients)
                except Exception as e:
                    print(e)

            for s in readable:  # Для каждого сокета готового к чтению
                data = None
                if s is self.server:  # Если это сокет принимающий соединения
                    connection, client_address = s.accept()
                    connection.setblocking(0)  # Этот клиентский сокет тоже будет неблокируемым
                    self.sockets.append(connection)  # Добавляем клиентский сокет в список сокетов
                    self.message_queues[connection] = queue.Queue()  # Создаём очередь сообщений для сокета
                    # print(help(connection))
                    print(connection.getpeername())
                    # print(connection.)
                    self.new_clients.append(connection.getpeername())
                else:
                    try:
                        if s in self.clients:
                            data = s.recv(1024)  # Читаем без блокировки
                            self.messages[s.getpeername()].append(data)
                            print(data.decode())
                            # for sock in writable:
                            # print(type(sock))
                            # sock.send(bytes("Не надо мне ничего присылать", encoding="utf-8"))
                    except:
                        self.close_connection(s)  # В случае ошибки закрываем этот сокет и удаляем
                    else:  # Если ошибка не произошла
                        if data:  # И данные получены
                            for c in self.message_queues:  # Обходим все очереди сообщений
                                if c != s:  # Кроме очереди текущего сокета
                                    self.message_queues[c].put(data)  # Отправляем данные в каждую очередь
                        else:
                            # Если данных нет в сокете готовом для чтения
                            # значит он в состоянии закрытия на клиентской
                            # стороне. Закрываем его на стороне сервера.
                            self.close_connection(s)

            for s in writable:  # Для каждого сокета готового к записи
                try:
                    next_msg = self.message_queues[s].get_nowait()  # Получаем сообщение из очереди
                except queue.Empty:
                    pass  # Игнорируем пустые очереди
                except KeyError:
                    pass  # Игнорируем очереди удалённые до того, как до них дошла очередь обработки
                else:
                    s.send(next_msg)  # Отправляем без блокировки

            for s in exceptional:  # Для каждого сбойного сокета
                self.close_connection(s)  # Закрываем сбойный сокет

    def run(self):
        # Configuring the Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.bind((self.ip, self.port))
        self.server.listen()
        self.main()

    def stop(self):
        self.server = None
        self.sockets = [self.server]
        self.message_queues = {}
        self.clients = {}
        self.new_clients = []
        self.messages = {}
        self.used_nicknames = []
        self.wait_access = []