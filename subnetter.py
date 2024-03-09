import sys
import math

def format_address(string):
    split_address = string.split('.')
    if len(split_address) != 4:
        raise ValueError
    for i in range(4):
        if int(split_address[i]) < 0 or int(split_address[i]) > 255:
            raise ValueError
    return split_address

def print_help():
    print("\
            usage: subnetter [--OPTIONS] [VALUE]\n\
            options:\n\
            --help\t\t\tDisplay arguments and values\n\
            --address [ADDRESS]\tNetwork address to analyze\n\
            --subnets [NB_SUBNETS]\tMinimum number of subnets required\n\
            --hosts [NB_HOSTS]\tMinimum number of hosts required\n\
            --bits [NB_BITS]\tNumber of bits used for the network and subnetwork\n\
            --range [Nth RANGE]\t\n\
            ")

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

            case "--bits":
                try:
                    i += 1
                    values["bits"] = int(args[i])
                except:
                    print("Error: \"--bits\" value must be an integer")

            case "--range":
                try:
                    i += 1
                    values["range"] = int(args[i])
                except: 
                    print("Error: \"--range\" value must be an integer")
        i += 1
    return values 

def get_address_class(address):
    if int(address[0]) < 2**7:
        return 'A'
    elif int(address[0]) < 2**7 + 2**6:
        return 'B'
    elif int(address[0]) < 2**7 + 2**6 + 2**5:
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



def main():
    values = format_args(sys.argv)
    if values.get("address"):
        address_class = get_address_class(values["address"])
        default_mask = get_default_mask(address_class)
        if values.get("subnets"):
            nb_subnets = calculate_min_square(values["subnets"] + 2)
            print(nb_subnets)
            bits_borrowed = int(math.log2(nb_subnets))
            custom_mask = calculate_custom_mask(default_mask, bits_borrowed)
            nb_hosts = calculate_host_addresses(custom_mask)
        elif values.get("hosts"):
            nb_hosts = calculate_min_square(values["hosts"] + 2)
            custom_mask = calculate_alternate_custom_mask(nb_hosts)
            nb_subnets = calculate_nb_subnets(default_mask, custom_mask)
            bits_borrowed = int(math.log2(nb_subnets))
        elif values.get("bits"):
            nb_hosts = 2**(32 - values["bits"])
            custom_mask = calculate_alternate_custom_mask(nb_hosts)
            nb_subnets = calculate_nb_subnets(default_mask, custom_mask)
            bits_borrowed = int(math.log2(nb_subnets))
        print(
f'Address: {".".join(values["address"])}\t\tAddress Class: {address_class}\n\
Default Mask: {format_to_address(default_mask)}\tCustom Mask: {format_to_address(custom_mask)}\n\
Total subnets: {nb_subnets}\t\tTotal usable hosts: {nb_subnets - 2}\n\
Total hosts: {nb_hosts}\t\t\tTotal usable hosts: {nb_hosts - 2}\n\
Bits borrowed: {bits_borrowed}\n')
        if values.get("range"):
            for i in range(int(values["range"])):
                calculate_subnet_range(i)

    else:
        print("Error: \"--address\" must be provided")

if __name__ == "__main__":
    main()
