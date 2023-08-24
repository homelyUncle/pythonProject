import re
import click
import minimalmodbus


def check_for_numbers(input_str):
    if len(re.findall("[^0-9 -]", input_str)) > 0:
        print("\nCheck the input string! You should input only numbers, space and hyphen.\n")
        return False
    return True


def get_addresses(input_str):
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


@click.command()
@click.option('-ad', prompt='Input a range of addresses', help='Addresses you need to check', required=True,
              default='15', show_default=False)
@click.option('-sp', default=9600, show_default=True, help='speed (bod)')
@click.option('-sb', default=1, show_default=True, help='stopbits [1 | 2]')
@click.option('-pr', default='none', show_default=True, help='paring [none | even | odd]')
@click.option('-bs', default=8, show_default=True, help='bytesize [5 | 6 | 7 | 8]')
@click.option('-to', default=0.5, show_default=True, help='timeout (sec)')
def start(ad, sp, sb, pr, bs, to):
    addresses = []

    addresses = get_addresses(ad)

    if len(addresses) > 1:
        words = ["These", "es"]
    else:
        words = ["This", ""]
    click.secho(f"{words[0]} address{words[1]} will be checked: {addresses} at speed {sp}\nstopbits\t{sb}\n"
                f"parity\t\t{pr}\nbytesize\t{bs}\ntimeout\t\t{to}", fg='green')

if __name__ == '__main__':
    start()
