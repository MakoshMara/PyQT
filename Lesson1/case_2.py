import ipaddress

from case_1 import host_ping

def host_range_ping():
    ip_addresses = []
    start_ip = ipaddress.ip_address(input('Введите стартовый ip адрес:'))
    stop_ip = ipaddress.ip_address(input('Введите конечный ip адрес:'))
    start_address_bytes = [int(x) for x in str(start_ip).split('.')]
    stop_address_bytes = [int(x) for x in str(stop_ip).split('.')]
    if stop_ip < start_ip:
        print('Введен некорректный диапазон адресов. Конечный адрес меньше начального')
    if stop_address_bytes[2] >start_address_bytes[2]:
        print('Введен некорректный диапазон адресов. Предпоследний октет конечного адреса отличен от стартового')
    if stop_address_bytes[3] > 255:
        print('Введен некорректный диапазон адресов. Конечный адрес выходит за границы подсети')
    step = int(input('Введите шаг изменения ip адреса:'))

    ip_adrr = start_ip
    while ip_adrr <= stop_ip:
        ip_addresses.append(str(ip_adrr))
        ip_adrr +=step

    return host_ping(ip_addresses)

if __name__ == '__main__':
    res = host_range_ping()
    for el in res:
        print(f'Узел {el[0]} {el[1]}')
