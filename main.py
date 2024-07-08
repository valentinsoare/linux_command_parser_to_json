import ip_route_command

"""
Right now I'm writing modules made for each linux command that we need its output to JSON. 
hen several commands will be available as JSON, then the main logic of the app will be created.

More to come....
"""


def print_hi():
    ip_route_command.main()


if __name__ == '__main__':
    print_hi()
