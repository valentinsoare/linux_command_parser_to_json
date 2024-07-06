import ip_route_command

input_value = """
default via 192.168.100.1 dev enp52s0 proto dhcp src 192.168.100.35 metric 100 
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 
192.168.100.0/24 dev enp52s0 proto kernel scope link src 192.168.100.35 metric 100
"""


def print_hi():
    ip_route_command.main(input_value)


if __name__ == '__main__':
    print_hi()
