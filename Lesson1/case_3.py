from tabulate import tabulate

from case_2 import host_range_ping


def host_range_ping_tab():
    dict_to_print = {'Доступен':[],'Недоступен':[]}
    res = host_range_ping()
    for el in res:
        if el[1] == 'доступен':
            dict_to_print['Доступен'].append(el[0])
        else:
            dict_to_print['Недоступен'].append(el[0])
    print(tabulate(dict_to_print, headers='keys', tablefmt="grid"))
    print(tabulate(res))

if __name__ == '__main__':
    host_range_ping_tab()