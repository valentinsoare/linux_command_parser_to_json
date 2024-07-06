#!/usr/bin/python3

import argparse
import textfsm


def _take_input() -> str:
    """
    Parses command line arguments to get the routing table input as a string.
    Returns:
        str: The routing table input provided by the user.
    """
    parser = argparse.ArgumentParser(description='Parse linux routing table output.')
    parser.add_argument('input_string', type=str, help='Routing table input (ip route output) as a string.')
    args = parser.parse_args()

    return args.input_string


def _take_input_mock() -> str:
    """
    Provides a mock input string representing the output of a routing table command.
    This is useful for testing purposes when actual command line input is not available.

    Returns:
    str: A mock string representing the output of a routing table command.
    """
    input_from_user: str = """
default via 192.168.100.1 dev enp52s0 proto dhcp src 192.168.100.35 metric 100
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
192.168.100.0/24 dev enp52s0 proto kernel scope link src 192.168.100.35 metric 100
"""
    return input_from_user


def _parse_input(name_of_file_template: str, input_from_user: str) -> tuple:
    """
    Parses the input string using a TextFSM template to extract routing information.

    Args:
        name_of_file_template (str): The path to the TextFSM template file.
        input_from_user (str): The routing table input as a string.

    Returns:
        tuple: A tuple containing the parsed results and the TextFSM object.
    """
    with open(name_of_file_template) as template_file:
        fsm = textfsm.TextFSM(template_file)
        parsed_results = fsm.ParseText(input_from_user)

    return parsed_results, fsm


def _extract_output(content_parsed: list, fsm_like: object) -> list:
    """
    Extracts and formats the parsed routing information into a list of dictionaries.

    Args:
        content_parsed (list): The parsed routing information as a list of lists.
        fsm_like (object): The TextFSM object used for parsing.

    Returns:
        list: A list of dictionaries, each representing a routing entry.
    """

    output: list = ["["]
    elements = fsm_like.header

    for row in content_parsed:
        result: dict = {}

        for i in range(len(elements)):
            if row[i] != '':
                result[elements[i]] = row[i]

        output.append(result)

    output.append("]")

    return output


def _print_the_output(output: list) -> None:
    """
    Prints the extracted routing information.
    This method formats the output for readability before printing.

    Args:
        output (list): The extracted routing information as a list of dictionaries.
    """
    for i, item in enumerate(output):
        print(item, end="," if 0 < i < len(output) - 2 else "")


def main():
    """
    Main function that orchestrates the parsing and printing of routing table information.
    """
    name_of_file: str = "parser_templates/ip_route.template"

    result_from_command_as_a_list_parsed, as_fsm = _parse_input(name_of_file, _take_input_mock())
    extracted_result = _extract_output(result_from_command_as_a_list_parsed, as_fsm)
    _print_the_output(extracted_result)


if __name__ == '__main__':
    main()
