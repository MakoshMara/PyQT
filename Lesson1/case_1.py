import ipaddress
from subprocess import Popen, PIPE


def host_ping(ip_addresses):
    param = '-n'
    result = []
    for ip_address in ip_addresses:
        args = ['ping', param, '2', ip_address]
        reply = Popen(args, stdout=PIPE, stderr=PIPE)
        code = reply.wait()
        if code == 0:
            result.append((ip_address, 'доступен'))
        else:
            result.append((ip_address,'недоступен'))
    return result


if __name__ == '__main__':
    ip1 = str(ipaddress.ip_address('192.168.0.1'))
    ip2 = str(ipaddress.ip_address('192.168.0.2'))
    ip_addresses = ['yandex.ru', ip1, ip2]
    res = host_ping(ip_addresses)
    for el in res:
        print(f'Узел {el[0]} {el[1]}')
