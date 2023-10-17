#!/usr/bin/env python3

import re
import minimalmodbus


PARITY = {
    "none": "N",
    "even": "E",
    "odd": "O"
}


def check_for_numbers(input_str: str) -> bool:
    if len(re.findall("[^0-9 -]", input_str)) > 0:
        print("\nНеверный формат адресов\n")
        return False
    return True


def get_addresses(input_str: str) -> list:
    # проверка состава символов строки с адресами
    if not check_for_numbers(input_str):
        return []

    addr_out = []

    for num in input_str.split():
        if num.isdigit(): # сбор одиночных адресов
            addr_out.append(int(num))
        else: # сбор диапазонов адресов
            nums = num.split('-')
            if len(nums[0]) == 0 or len(nums[1]) == 0:
                print("\nНеверный диапазон\n")
                return []
            else:
                nums = sorted(int(x) for x in nums)
            for x in range(nums[0], nums[1] + 1):
                addr_out.append(x)
    return sorted(addr_out)


def get_settings() -> tuple:
    addresses = ""
    baudrate = 9600
    bytesize = 8
    parity = "none"
    stopbits = 1
    timeout = 0.5
    port = "/dev/ttyRS485-1"
    with open("setting.txt", "r") as setting_file:
        for line in setting_file:
            if line.startswith("addresses: "):
                addresses = get_addresses(line.split(": ")[1].rstrip("\n"))
            elif line.startswith("baudrate: "):
                baudrate = int(line.split(": ")[1])
            elif line.startswith("bytesize: "):
                bytesize = int(line.split(": ")[1])
            elif line.startswith("parity: "):
                parity = PARITY.get(line.split(": ")[1].strip())
            elif line.startswith("stopbits: "):
                stopbits = int(line.split(": ")[1])
            elif line.startswith("timeout: "):
                timeout = float(line.split(": ")[1])
            elif line.startswith("port: "):
                port = line.split(": ")[1].strip()
    return addresses, baudrate, bytesize, parity, stopbits, timeout, port


def checking(port: str, addr: int, br: int, bs: int, pr: str, sb: int, to: float) -> bool:
    device = minimalmodbus.Instrument(port=port, slaveaddress=addr, 
                                      close_port_after_each_call=True)
    device.serial.baudrate = br
    device.serial.bytesize = bs
    device.serial.parity = pr
    device.serial.stopbits = sb
    device.serial.timeout = to

    try:
        device.read_register(1)
        print(f"[{device.address}] +")
        return True
    except IOError:
        print(f"[{device.address}] -")
        return False


def start() -> None:
    addresses_online: list = []
    addresses_to_check, baudrate, bytesize, parity, stopbits, timeout, port = get_settings()
    if len(addresses_to_check) != 0:
        if len(addresses_to_check) > 1:
            words = ["Эти", "а", "ут", "ы"]
        else:
            words = ["Этот", "", "ет", ""]
        print(f"{words[0]} адрес{words[1]} буд{words[2]} проверен{words[3]}: {addresses_to_check}\n"
              "со следующими настройками:\n"
              f"Порт: {port} : {baudrate} : {bytesize} {parity} {stopbits} (timeout: {timeout})")
    else:
        print("Отсутствуют адреса для проверки. Проверьте файл настроек.")
        return None
    
    for address in addresses_to_check:
        if checking(port, address, baudrate, bytesize, parity, stopbits, timeout):
            addresses_online.append(address)

    print("-    -   -  - = = = -  -   -    -\n"
          f"Устройства на связи со следующими адресами:\n{addresses_online}")


if __name__ == '__main__':
    start()
