import re
import click
import minimalmodbus


def ask_addr() -> str:
    return input("Input a range of addresses separated by a hyphen\n"
                 "and/or a single addresses separated by a space [121 95-90 15 41-43]: ")


def check_for_numbers(input_str: str) -> bool:
    if len(re.findall("[^0-9 -]", input_str)) > 0:
        print("\nCheck the input string! You should input only numbers, space and hyphen.\n")
        return False
    return True


def get_addresses(input_str: str) -> list:
    # checking the string for extra characters
    if not check_for_numbers(input_str):
        return []

    addr_out = []

    for num in input_str.split():
        if num.isdigit(): # collect alone digits
            addr_out.append(int(num))
        else: # collect range of digits
            nums = num.split('-')
            if len(nums[0]) == 0 or len(nums[1]) == 0:
                print("\nWrong range!\n")
                return []
            else:
                nums = sorted(int(x) for x in nums)
            for x in range(nums[0], nums[1] + 1):
                addr_out.append(x)
    return sorted(addr_out)


addresses = []

while True:
    addresses = get_addresses(ask_addr())
    if len(addresses) == 0:
        continue
    else:
        break

if len(addresses) > 1:
    words = ["These", "es"]
else:
    words = ["This", ""]
print(f"{words[0]} address{words[1]} will be checked: {addresses}")

"""@click.command()
@click.argument()
def start():
    pass

if __name__ == '__main__':
    start()"""
