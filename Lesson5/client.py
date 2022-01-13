import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication

from client_file.main_window import ClientMainWindow
from client_file.transp import ClientTransport
from client_file.user_name_dialog import UserNameDialog
from client_file.client_database import ClientDatabase
from common.variables import DEFAULT_IP_ADRESS, DEFAULT_PORT

from decos import log
from errors import ServerError

CLIENT_LOGGER = logging.getLogger('client_file')

# sock_lock = threading.Lock()
# database_lock = threading.Lock()
#
#
# class ClientSender(threading.Thread, metaclass=ClientMaker):
#     def __init__(self, account_name, sock, database):
#         self.account_name = account_name
#         self.sock = sock
#         self.database = database
#         super().__init__()
#
#
#     def create_exit_message(self):
#         return {
#             ACTION: EXIT,
#             TIME: time.time(),
#             ACCOUNT_NAME: self.account_name
#         }
#
#
#     def create_message(self):
#         to_user = input('Введите получателя сообщения: ')
#         message = input('Введите сообщение для отправки: ')
#
#         with database_lock:
#             if not self.database.check_user(to_user):
#                 CLIENT_LOGGER.error(f'Попытка отправить сообщение незарегистрированому получателю: {to_user}')
#                 return
#
#         out_massage = {
#             ACTION: MESSAGE,
#             SENDER: self.account_name,
#             DESTINATION: to_user,
#             TIME: time.time(),
#             MESSAGE_TEXT: message
#         }
#         CLIENT_LOGGER.debug(f'Сформированно сообщение серверу: {out_massage}')
#         with database_lock:
#             self.database.save_message(self.account_name, to_user, message)
#
#         with sock_lock:
#             try:
#                 send_meccage(self.sock, out_massage)
#                 CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
#             except:
#                 CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
#                 sys.exit(1)
#
#     def run(self):
#         self.print_help()
#         while True:
#             command = input('Введите команду: ')
#             if command == 'message':
#                 self.create_message()
#             elif command == 'help':
#                 self.print_help()
#             elif command == 'exit':
#                 with sock_lock:
#                     try:
#                         send_meccage(self.sock, self.create_exit_message())
#                         print('Отправили на сервер сообщение о закрытии сессии')
#                     except Exception as e:
#                         print(e)
#                         pass
#                     print('Завершение соединения.')
#                     CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
#                 time.sleep(0.5)
#                 break
#             elif command == 'contacts':
#                 with database_lock:
#                     contacts_list = self.database.get_contacts()
#                 for contact in contacts_list:
#                     print(contact)
#
#             elif command == 'edit':
#                 self.edit_contacts()
#
#             # история сообщений.
#             elif command == 'history':
#                 self.print_history()
#             else:
#                 print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')
#
#     def print_help(self):
#         """Функция выводящяя справку по использованию"""
#         print('Поддерживаемые команды:')
#         print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
#         print('history - история сообщений')
#         print('contacts - список контактов')
#         print('edit - редактирование списка контактов')
#         print('help - вывести подсказки по командам')
#         print('exit - выход из программы')
#
#     def print_history(self):
#         ask = input('Показать входящие сообщения - in, исходящие - out, все - просто Enter: ')
#         with database_lock:
#             if ask == 'in':
#                 history_list = self.database.get_history(to_who=self.account_name)
#                 for message in history_list:
#                     print(f'\nСообщение от пользователя: {message[0]} от {message[3]}:\n{message[2]}')
#             elif ask == 'out':
#                 history_list = self.database.get_history(from_who=self.account_name)
#                 for message in history_list:
#                     print(f'\nСообщение пользователю: {message[1]} от {message[3]}:\n{message[2]}')
#             else:
#                 history_list = self.database.get_history()
#                 for message in history_list:
#                     print(f'\nСообщение от пользователя: {message[0]}, пользователю {message[1]} '
#                           f'от {message[3]}\n{message[2]}')
#
#     def edit_contacts(self):
#         ans = input('Для удаления введите del, для добавления add: ')
#         if ans == 'del':
#             edit = input('Введите имя удаляемного контакта: ')
#             with database_lock:
#                 if self.database.check_contact(edit):
#                     self.database.del_contact(edit)
#                 else:
#                     CLIENT_LOGGER.error('Попытка удаления несуществующего контакта.')
#         elif ans == 'add':
#             edit = input('Введите имя создаваемого контакта: ')
#             if self.database.check_user(edit):
#                 print('Добавляемый юзер известен')
#                 with database_lock:
#                     self.database.add_contact(edit)
#                 with sock_lock:
#                     try:
#                         add_contact(self.sock, self.account_name, edit)
#                     except:
#                         CLIENT_LOGGER.error('Не удалось отправить информацию на сервер.')
#
#
# class ClientReader(threading.Thread, metaclass=ClientMaker):
#     def __init__(self, account_name, sock, database):
#         self.account_name = account_name
#         self.sock = sock
#         self.database = database
#         super().__init__()
#
#     def run(self):
#         while True:
#             time.sleep(1)
#             with sock_lock:
#                 try:
#                     message = get_message(self.sock)
#                 except IncorrectDataRecivedError:
#                     CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
#                 except OSError as err:
#                     if err.errno:
#                         CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
#                         break
#                 except (ConnectionError, ConnectionAbortedError,
#                         ConnectionResetError, json.JSONDecodeError):
#                     CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
#                     break
#                 else:
#                     if ACTION in message and message[ACTION] == MESSAGE and \
#                             SENDER in message and DESTINATION in message \
#                             and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
#                         print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
#                               f'\n{message[MESSAGE_TEXT]}')
#                         with database_lock:
#                             try:
#                                 self.database.save_message(message[SENDER], self.account_name, message[MESSAGE_TEXT])
#                             except Exception as e:
#                                 print(e)
#                                 CLIENT_LOGGER.error('Ошибка взаимодействия с базой данных')
#                         CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
#                                            f'\n{message[MESSAGE_TEXT]}')
#                     else:
#                         CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
#
#
#
# # @log
# # def user_interactive(sock, username):
# #     """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
# #     print_help()
# #     while True:
# #         command = input('Введите команду: ')
# #         if command == 'message':
# #             create_message(sock, username)
# #         elif command == 'help':
# #             print_help()
# #         elif command == 'exit':
# #             send_meccage(sock, create_exit_message(username))
# #             print('Завершение соединения.')
# #             CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
# #             # Задержка неоходима, чтобы успело уйти сообщение о выходе
# #             time.sleep(0.5)
# #             break
# #         else:
# #             print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')
#


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

if __name__ == '__main__':
    server_adr, server_port, client_name = arg_parser()

    client_app = QApplication(sys.argv)
    if not client_name:
        user_name_dialog = UserNameDialog()
        client_app.exec_()
        if user_name_dialog.ok_pressed:
            client_name = user_name_dialog.client_name.text()
            del user_name_dialog
        else:
            exit(0)

    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_adr} , порт: {server_port}, имя пользователя: {client_name}')

    database = ClientDatabase(client_name)

    try:
        transport = ClientTransport(server_port, server_adr, database, client_name)
    except ServerError as error:
        print(error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()

#


#
#
# # Функция инициализатор базы данных. Запускается при запуске, загружает данные в базу с сервера.
# def database_load(sock, database, username):
#     try:
#         users_list = user_list_request(sock, username)
#     except ServerError:
#         CLIENT_LOGGER.error('Ошибка запроса списка известных пользователей.')
#     else:
#         database.add_users(users_list)
#
#     try:
#         contacts_list = contacts_list_request(sock, username)
#         CLIENT_LOGGER.info(f'Ваш список контактов {contacts_list}')
#     except ServerError:
#         CLIENT_LOGGER.error('Ошибка запроса списка контактов.')
#     else:
#         for contact in contacts_list:
#             database.add_contact(contact)
#
#
# def main():
#     server_adr, server_port, client_name = arg_parser()
#     print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {client_name}')
#     if not client_name:
#         client_name = input('Введите имя пользователя: ')
#
#     CLIENT_LOGGER.info(
#         f'Запущен клиент с парамертами: адрес сервера: {server_adr}, '
#         f'порт: {server_port}, имя пользователя: {client_name}')
#     try:
#         transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         transport.settimeout(1)
#
#         transport.connect((server_adr, server_port))
#         send_meccage(transport, create_presence(client_name))
#         answer = process_answer(get_message(transport))
#         CLIENT_LOGGER.info(f'Принят ответ от сервера:{answer}')
#     except json.JSONDecodeError:
#         CLIENT_LOGGER.error(f'Не удалось декодировать JSON от сервера')
#         sys.exit(1)
#     except ConnectionRefusedError:
#         CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_adr}:{server_port} '
#                                f'Сервер отверг запрос на подключение')
#         sys.exit(1)
#     except ReqFieldMissingError as missing_error:
#         CLIENT_LOGGER.error(f'В ответе сервера отсутвует необходимое поле '
#                             f'{missing_error.missing_field}')
#     else:
#         database = ClientDatabase(client_name)
#         database_load(transport, database, client_name)
#
#         module_reciver = ClientReader(client_name, transport, database)
#         module_reciver.daemon = True
#         module_reciver.start()
#
#         module_sender = ClientSender(client_name, transport, database)
#         module_sender.daemon = True
#         module_sender.start()
#         CLIENT_LOGGER.debug('Запущены процессы')
#
#         while True:
#             time.sleep(1)
#             if module_reciver.is_alive() and module_sender.is_alive():
#                 continue
#             break
#
#
# if __name__ == '__main__':
