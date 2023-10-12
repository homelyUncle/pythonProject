#!/usr/bin/env python3

import re
import minimalmodbus


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
    with open("setting.txt", "r") as setf:
        for line in setf:
            if line.startswith("addresses: "):
                addresses = get_addresses(line.split(": ")[1].rstrip("\n"))
            elif line.startswith("baudrate: "):
                baudrate = int(line.split(": ")[1])
            elif line.startswith("databits: "):
                bytesize = int(line.split(": ")[1])
            elif line.startswith("parity: "):
                parity = line.split(": ")[1]
            elif line.startswith("stopbits: "):
                stopbits = int(line.split(": ")[1])
            elif line.startswith("timeout: "):
                timeout = float(line.split(": ")[1])
            elif line.startswith("port: "):
                port = line.split(": ")[1]
    return addresses, baudrate, bytesize, parity, stopbits, timeout, port


def cheking(port: str, addr: int, br: int, bs: int, pr: str, sb: int, to: float) -> bool:
    device = minimalmodbus.Instrument(port=port, slaveaddress=addr, 
                                      close_port_after_each_call=True)
    device.serial.baudrate = br
    device.serial.bytesize = bs
    device.serial.parity = pr
    device.serial.stopbits = sb
    device.serial.timeout = to

    try:
        device.read_bit(1)
        return True
    except IOError:
        print(f"Ошибка проверки связи с устройством по адресу {device.address}")
        return False


def start():
    addresses_online = []
    addresses_to_check = []
    addresses_to_check, baudrate, bytesize, parity, stopbits, timeout, port = get_settings()
    if len(addresses_to_check) != 0:
        if len(addresses_to_check) > 1:
            words = ["Эти", "а", "ут", "ы"]
        else:
            words = ["Этот", "", "ет", ""]
        print(f"{words[0]} адрес{words[1]} буд{words[2]} проверен{words[3]}: {addresses_to_check}\n"
              "со следующими натройками:\n"
              f"Порт: {port} : {baudrate} : {bytesize} {parity} {stopbits} (timeout: {timeout})")
    
    for address in addresses_to_check:
        if cheking(port, address, baudrate, bytesize, parity, stopbits, timeout):
            addresses_online.append(address)

    print(f"Устройства на связи со следующими адресами:\n{addresses_online}")


if __name__ == '__main__':
    start()
