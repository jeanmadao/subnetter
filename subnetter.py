import sys
import math

def format_address(string):
    split_address = string.split('.')
    result = 0
    if len(split_address) != 4:
        raise ValueError
    for i in range(4):
        if int(split_address[i]) < 0 or int(split_address[i]) > 255:
            raise ValueError
        else:
            result += int(split_address[i]) << (24 - 8 * i)
    return result

def print_help():
    print("\
usage: subnetter [--OPTIONS] [VALUE]\n\
options:\n\
--help\t\t\tList available arguments\n\
--address [ADDRESS]\tNetwork address to analyze\n\
--subnets [NB_SUBNETS]\tMinimum number of subnets required\n\
--hosts [NB_HOSTS]\tMinimum number of usable hosts required\n\
--cidr [NB_BITS]\tCIDR Notation to represent the network portion\n\
--range [NTH_SUBNET]\tDisplay the NTH subnet host addresses range\n\
")

def print_results(address, address_class, default_mask, custom_mask, nb_subnets, nb_hosts, bits_borrowed):
    print(f'\
Address: {format_to_address(address).ljust(20)} Address Class: {address_class}\n\
Default Mask: {format_to_address(default_mask).ljust(15)} Custom Mask: {format_to_address(custom_mask)}\n\
Total subnets: {str(nb_subnets).ljust(14)} Total usable hosts: {nb_subnets - 2}\n\
Total hosts: {str(nb_hosts).ljust(16)} Total usable hosts: {nb_hosts - 2}\n\
Bits borrowed: {bits_borrowed}\n\
')

def format_args(args):
    values = {}
    i = 0
    while i < len(args):
        match args[i]:
            case "--help":
                print_help()

            case "--address":
                try:
                    i += 1
                    values["address"] = format_address(args[i])
                except:
                    print("Error: \"--address\" value must be in this format: \"[0-255].[0-255].[0-255].[0-255]\"")

            case "--subnets":
                try:
                    i += 1
                    values["subnets"] = int(args[i])
                except:
                    print("Error: \"--subnets\" value must be an integer")

            case "--hosts":
                try:
                    i += 1
                    values["hosts"] = int(args[i])
                except:
                    print("Error: \"--hosts\" value must be an integer")

            case "--cidr":
                try:
                    i += 1
                    values["cidr"] = int(args[i])
                except:
                    print("Error: \"--cidr\" value must be an integer")

            case "--range":
                try:
                    i += 1
                    values["range"] = int(args[i])
                except: 
                    print("Error: \"--range\" value must be an integer")
        i += 1
    return values 

def get_address_class(address):
    first_byte = address >> 24
    if first_byte < 2**7:
        return 'A'
    elif first_byte < 2**7 + 2**6:
        return 'B'
    elif first_byte < 2**7 + 2**6 + 2**5:
        return 'C'
    else:
        return 'D'

def get_default_mask(address_class):
    match address_class:
        case 'A':
            return (2**32 - 1) ^ (2**24 - 1)
        case 'B':
            return (2**32 - 1) ^ (2**16 - 1)
        case _: #C
            return (2**32 - 1) ^ (2**8 - 1)

def calculate_min_square(nb):
    binary = bin(nb)[2:]
    bits = len(binary) - 1
    if binary.count('1') > 1:
        bits += 1
    return 2**bits

def calculate_custom_mask(default_mask, bits_borrowed):
    custom_mask = default_mask
    for _ in range(bits_borrowed):
        custom_mask = (custom_mask >> 1) + 2**31
    return custom_mask

def calculate_alternate_custom_mask(nb_hosts):
    return 2**32-1 ^ nb_hosts-1
            
def calculate_host_addresses(custom_mask):
    return (custom_mask ^ (2**32-1)) + 1

def calculate_nb_subnets(default_mask, custom_mask):
    bits = bin(default_mask ^ custom_mask).count('1')
    return 2**bits

def format_to_address(number):
    return f'{number // 2**24 & 2**8-1}.{number // 2**16 & 2**8-1}.{number // 2**8 & 2**8-1}.{number & 2**8-1}'

def calculate_subnet_range(address, custom_mask, n):
    subnet_range_end = (custom_mask ^ (2**32-1))
    base = subnet_range_end + 1
    adder = base * (n - 1)

    results = (address | adder, address | adder | subnet_range_end)
    return results

def print_subnet_range(n, subnet_range):
    print(f'\
Range:\n\
{n}) {format_to_address(subnet_range[0])} to {format_to_address(subnet_range[1])}\n\
')


def main():
    values = format_args(sys.argv)
    if values.get("address"):
        address_class = get_address_class(values["address"])
        default_mask = get_default_mask(address_class)
        if values.get("subnets"):
            nb_subnets = calculate_min_square(values["subnets"])
            bits_borrowed = int(math.log2(nb_subnets))
            custom_mask = calculate_custom_mask(default_mask, bits_borrowed)
            nb_hosts = calculate_host_addresses(custom_mask)
        elif values.get("hosts"):
            nb_hosts = calculate_min_square(values["hosts"] + 2)
            custom_mask = calculate_alternate_custom_mask(nb_hosts)
            nb_subnets = calculate_nb_subnets(default_mask, custom_mask)
            bits_borrowed = int(math.log2(nb_subnets))
        elif values.get("cidr"):
            nb_hosts = 2**(32 - values["cidr"])
            custom_mask = calculate_alternate_custom_mask(nb_hosts)
            nb_subnets = calculate_nb_subnets(default_mask, custom_mask)
            bits_borrowed = int(math.log2(nb_subnets))
        else:
            print("Error: At least\"--subnets\", or \"--cidr\", or \"--hosts\" must be specified")
            return
        print_results(values["address"], address_class, default_mask, custom_mask, nb_subnets, nb_hosts, bits_borrowed)
        if values.get("range")  and 0 < values.get("range") <= nb_subnets :
             print_subnet_range(values.get("range"), calculate_subnet_range(values["address"], custom_mask, values['range']))
    else:
        print("Error: \"--address\" must be provided")

if __name__ == "__main__":
    main()
