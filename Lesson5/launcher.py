
import subprocess

process = []

while True:
    action = input('Выберите действие: q - выход , s - запустить сервер, k - запустить клиенты x - закрыть все окна:')
    if action == 'q':
        break
    elif action == 's':
        # Запускаем сервер!
        process.append(subprocess.Popen('python server.py',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
        # process.append(subprocess.Popen('python server_run.py', creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'k':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        # Запускаем клиентов:
        for i in range(clients_count):
            process.append(subprocess.Popen(f'python client.py -n test{i + 1}', creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'x':
        while process:
            process.pop().kill()

# """Лаунчер"""
#
# import subprocess
#
# PROCESSES = []
#
# while True:
#     ACTION = input('Выберите действие: q - выход, '
#                    's - запустить сервер и клиенты, '
#                    'x - закрыть все окна: ')
#
#     if ACTION == 'q':
#         break
#     elif ACTION == 's':
#         PROCESSES.append(subprocess.Popen('python server.py',
#                                           creationflags=subprocess.CREATE_NEW_CONSOLE))
#         PROCESSES.append(subprocess.Popen('python client_file.py -n test1',
#                                           creationflags=subprocess.CREATE_NEW_CONSOLE))
#         # PROCESSES.append(subprocess.Popen('python client_file.py -n test2',
#         #                                   creationflags=subprocess.CREATE_NEW_CONSOLE))
#         PROCESSES.append(subprocess.Popen('python client_file.py -n test3',
#                                           creationflags=subprocess.CREATE_NEW_CONSOLE))
#     elif ACTION == 'x':
#         while PROCESSES:
#             VICTIM = PROCESSES.pop()
#             VICTIM.kill()
