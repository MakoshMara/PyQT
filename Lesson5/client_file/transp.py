import socket
import sys
import time
import logging
import json
import threading
from PyQt5.QtCore import pyqtSignal, QObject

sys.path.append('../')
from common.utils import *
from common.variables import *
from errors import ServerError

logger = logging.getLogger('client_file')
socket_lock = threading.Lock()

class ClientTransport(threading.Thread, QObject):
    new_msg = pyqtSignal(str)
    connection_lost = pyqtSignal()

    def __init__(self,port,ip_address,database,username):
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.database = database
        self.transport = None
        self.username = username
        self.connection_init(port, ip_address)
        try:
            self.user_list_request()
            self.contacts_list_request()
        except OSError as err:
            if err.errno:
                logger.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            logger.error('Timeout соединения при обновлении списков пользователей.')

        except json.JSONDecodeError:
            logger.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
        self.running = True

    def connection_init(self,port,ip):
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)
        print(f'{self.transport}')
        connected = False
        for i in range(5):
            logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)
        if not connected:
            logger.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')
        logger.debug('Установлено соединение с сервером')

        try:
            with socket_lock:
                send_meccage(self.transport, self.create_presence())
                self.process_answer(get_message(self.transport))
        except (OSError, json.JSONDecodeError):
            logger.critical('Потеряно соединение с сервером!')
            raise ServerError('Потеряно соединение с сервером!')

        logger.info('Сервер ответил на приветственное сообщение.')

    def create_presence(self):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.username
            }
        }
        logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.username}')
        return out

    def process_answer(self, message):
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200: все норм'
            logger.error(f'При обработке сервером обнаружена ошибка:{message[ERROR]}')
            return f'400:{message[ERROR]}'

        elif ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                and MESSAGE_TEXT in message and message[DESTINATION] == self.username:
            logger.debug(f'Получено сообщение от пользователя {message[SENDER]}:{message[MESSAGE_TEXT]}')
            self.database.save_message(message[SENDER] , 'in' , message[MESSAGE_TEXT])
            self.new_msg.emit(message[SENDER])

    def contacts_list_request(self):
        logger.debug(f'Запрос контакт листа для пользователя {self.username}')
        req = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        logger.debug(f'Сформирован запрос {req}')
        with socket_lock:
            send_meccage(self.transport, req)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            logger.error('Не удалось обновить список контактов.')

    def user_list_request(self):
        logger.debug(f'Запрос списка известных пользователей {self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        send_meccage(self.transport, req)
        ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            logger.error('Не удалось обновить список известных пользователей.')

    def add_contact(self, contact):
        logger.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_meccage(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 200:
            pass
        else:
            raise ServerError('Ошибка создания контакта')
        print('Удачное создание контакта.')

    def remove_contact(self, contact):
        logger.debug(f'Создание контакта {contact}')
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_meccage(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 200:
            pass
        else:
            raise ServerError('Ошибка удаления клиента')
        print('Удачное удаление')

    def transport_shutdown(self):
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_meccage(self.transport, message)
            except OSError:
                pass
        logger.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def create_message(self, to_user, message):
        logger.debug(f'Начинаем формировать сообщение для: {to_user}')
        out_massage = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        logger.debug(f'Сформированно сообщение серверу: {out_massage}')
        with socket_lock:
            try:
                send_meccage(self.transport, out_massage)
                logger.info(f'Отправлено сообщение для пользователя {to_user}')
            except:
                logger.critical('Потеряно соединение с сервером.')

    def run(self):
        logger.debug('Запущен процесс - приёмник собщений с сервера.')
        while self.running:
            time.sleep(1)
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        logger.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
                    logger.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                else:
                    logger.debug(f'Принято сообщение с сервера: {message}')
                    self.process_answer(message)
                finally:
                    self.transport.settimeout(5)