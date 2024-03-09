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
| --hosts [NB_HOSTS] | Minimum number of hosts required |
| --bits [NB_BITS] | Number of bits used for the network and subnetwork |

## Example
```
python subnetter.py --address 165.100.0.0 --subnets 1000
```

Output:
```
Address: 165.100.0.0		Address Class: B
Default Mask: 255.255.0.0	Custom Mask: 255.255.255.192
Total subnets: 1024		Total usable hosts: 1022
Total hosts: 64			Total usable hosts: 62
Bits borrowed: 10
```
