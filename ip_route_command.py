#!/usr/bin/python3

import argparse
import json
import os

import textfsm


def _take_input_from_commandline() -> str:
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
192.168.1.0/24 dev eth0  proto kernel  scope link  src 192.168.1.10
192.168.2.0/24 dev eth1  proto kernel  scope link  src 192.168.2.10
10.0.0.0/8 via 192.168.1.1 dev eth0
default via 192.168.1.1 dev eth0
"""
    return input_from_user


def _take_input_directly_from_iproute_command() -> str:
    return os.popen('ip route').read()


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

    output: list = []
    elements = fsm_like.header

    for row in content_parsed:
        result: dict = {}

        for i in range(len(elements)):
            if row[i] != '':
                result[elements[i]] = row[i]

        output.append(result)

    return output


def _validate_output(output_elements: list, classic_printing: bool) -> list:
    """
    Validates and formats the output elements for JSON-like representation.

    This function checks if the output elements list is empty or if the first element lacks a 'gateway' key,
    which are conditions indicating the input might not be from a valid Linux ip route command. If the validation
    fails, it prints an error message and exits the program. Otherwise, it encloses the output elements in brackets
    to mimic a JSON array format, enhancing readability and consistency for further processing or display.

    Args:
        output_elements (list): The list of dictionaries representing parsed routing information.

    Returns:
        list: The validated and formatted list of dictionaries, enclosed in brackets if valid.
              Exits the program if the validation fails.

    Raises:
        SystemExit: If the input is not from a Linux ip route command or the list is empty.
    """

    error_message: str = "ERROR - Input given is not from linux ip route command"
    it_exists = False

    if len(output_elements) == 0:
        print(error_message)
        exit(0)

    for i in range(len(output_elements)):
        if "gateway" in output_elements[i].keys():
            it_exists = True
            break

    if not it_exists:
        print(error_message)
        exit(0)

    if classic_printing:
        output_elements.append("]")
        output_elements.insert(0, "[")

    return output_elements


def _print_the_output(output: list) -> None:
    """
    Prints the extracted routing information.
    This method formats the output for readability before printing.

    Args:
        output (list): The extracted routing information as a list of dictionaries.
    """
    for i, item in enumerate(output):
        print(item, end="," if 0 < i < len(output) - 2 else "")


def _pretty_print_the_output(output: list) -> None:
    """
    Pretty prints the routing information as a formatted JSON string.

    This method takes the list of dictionaries representing routing entries and uses the json.dumps() method
    to convert it into a formatted JSON string. This enhances readability, making it easier to understand the
    routing information structure. The 'indent' parameter in json.dumps() is set to 2, which specifies the number
    of spaces to use for indentation.

    Args:
        output (list): The list of dictionaries representing routing entries.
    """
    print(json.dumps(output, indent=2))


def parse_and_transform():
    """
    Main function that orchestrates the parsing and printing of routing table information.
    """
    name_of_file: str = "parser_templates/ip_route.template"

    result_from_command_as_a_list_parsed, as_fsm = _parse_input(name_of_file, _take_input_mock())
    extracted_result = _extract_output(result_from_command_as_a_list_parsed, as_fsm)
    _print_the_output(_validate_output(extracted_result, True))


if __name__ == '__main__':
    parse_and_transform()
