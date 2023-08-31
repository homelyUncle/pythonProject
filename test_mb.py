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
    databits = 8
    parity = "none"
    stopbits = 1
    timeout = 500
    with open("setting.txt", "r") as setf:
        for line in setf:
            if line.startswith("addresses: "):
                addresses = get_addresses(line.split(": ")[1].rstrip("\n"))
            elif line.startswith("baudrate: "):
                baudrate = int(line.split(": ")[1])
            elif line.startswith("databits: "):
                databits = int(line.split(": ")[1])
            elif line.startswith("parity: "):
                parity = line.split(": ")[1]
            elif line.startswith("stopbits: "):
                stopbits = int(line.split(": ")[1])
            elif line.startswith("timeout: "):
                timeout = int(line.split(": ")[1])
    return addresses, baudrate, databits, parity, stopbits, timeout


def start():
    addresses = []
    addresses, baudrate, databits, parity, stopbits, timeout = get_settings()
    if len(addresses) != 0:
        if len(addresses) > 1:
            words = ["Эти", "а", "ут", "ы"]
        else:
            words = ["Этот", "", "ет", ""]
        print(f"{words[0]} адрес{words[1]} буд{words[2]} проверен{words[3]}: {addresses}\n"
              "со следующими натройками:\n"
              f"{baudrate} : {databits}{parity}{stopbits}")


if __name__ == '__main__':
    start()
