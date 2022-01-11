import argparse
import logging
import sys
import socket
import json
import logs.config_client_log
import time
import threading
import dis

from common.utils import send_meccage, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, DEFAULT_IP_ADRESS, DEFAULT_PORT, \
    RESPONSE, ERROR, MESSAGE, EXIT, DESTINATION
import time

from common.variables import SENDER, MESSAGE_TEXT
from decos import log
from errors import ReqFieldMissingError, IncorrectDataRecivedError
from metaclasses import ClientMaker

CLIENT_LOGGER = logging.getLogger('client')

class ClientSender(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    @log
    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
    }

    @log
    def create_message(self):
        to_user = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')
        out_massage = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформированно сообщение серверу: {out_massage}')
        try:
            send_meccage(self.sock, out_massage)
            CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
        except:
            CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                send_meccage(self.sock, self.create_exit_message())
                print('Завершение соединения.')
                CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


    def print_help(self):
        """Функция выводящяя справку по использованию"""
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')

class ClientReader(threading.Thread , metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and \
                        SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                          f'\n{message[MESSAGE_TEXT]}')
                    CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                               f'\n{message[MESSAGE_TEXT]}')
                else:
                    CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
                break

# @log
# def user_interactive(sock, username):
#     """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
#     print_help()
#     while True:
#         command = input('Введите команду: ')
#         if command == 'message':
#             create_message(sock, username)
#         elif command == 'help':
#             print_help()
#         elif command == 'exit':
#             send_meccage(sock, create_exit_message(username))
#             print('Завершение соединения.')
#             CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
#             # Задержка неоходима, чтобы успело уйти сообщение о выходе
#             time.sleep(0.5)
#             break
#         else:
#             print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out

@log
def process_answer(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: все норм'
        CLIENT_LOGGER.error(f'При обработке сервером обнаружена ошибка:{message[ERROR]}')
        return f'400:{message[ERROR]}'
    raise ValueError

@log
def arg_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')

    return server_address, server_port, client_name

@log
def main():
    server_adr, server_port, client_name = arg_parser()
    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {client_name}')
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_adr}, '
        f'порт: {server_port}, имя пользователя: {client_name}')
    try:
        transport = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        transport.connect((server_adr,server_port))
        send_meccage(transport, create_presence(client_name))
        CLIENT_LOGGER.info(f'Серверу отправлено сообщение')
        answer = process_answer(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера:{answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error(f'Не удалось декодировать JSON от сервера')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_adr}:{server_port} '
                               f'Сервер отверг запрос на подключение')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутвует необходимое поле '
                            f'{missing_error.missing_field}')
    else:
        module_reciver = ClientReader(client_name, transport)
        module_reciver.daemon = True
        module_reciver.start()

        module_sender = ClientSender(client_name , transport)
        module_sender.daemon = True
        module_sender.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            if module_reciver.is_alive() and module_sender.is_alive():
                continue
            break

if __name__ == '__main__':
    main()