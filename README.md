# Subnetter
Subnetter is a CLI utility to calculate all your subnetting needs!

## Usage
```
python subnetter.py --address [ADDRESS] [--OPTION] [VALUE]
```
The following options are available
| arguments | description |
|--------|---------|
| --help | List available arguments |
| --address [ADDRESS] | Network address to analyze |
| --subnets [NB_SUBNETS] | Minimum number of subnets required |
| --hosts [NB_HOSTS] | Minimum number of usable hosts required |
| --cidr [NB_BITS] | CIDR Notation to represent the network portion |
| --range [NTH_SUBNET] | Display the NTH subnet host addresses range |

## Example
```
python subnetter.py --address 192.10.10.0 --subnets 14 --range 4 
```

Output:
```
Address: 192.10.10.0		Address Class: C
Default Mask: 255.255.255.0	Custom Mask: 255.255.255.240
Total subnets: 16		Total usable hosts: 14
Total hosts: 16			Total usable hosts: 14
Bits borrowed: 4

Range:
4) 192.10.10.48 to 192.10.10.63
```
