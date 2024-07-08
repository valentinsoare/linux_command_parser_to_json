#!/usr/bin/python3

# -*- coding: utf-8 -*-
#
# This script along with its template called ip_route.template from parser_templates are owned by Valentin Soare.
# Licensed under the GNU General Public License, version 3 (GPL-3.0).import json.
# See the LICENSE file in the root directory for details.
# The use of this script by the London Stock Exchange does not confer
# any ownership rights to the employer.
#                                                                                            
# Author: Valentin Soare

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
    parser.add_argument('ip_route_output', type=str, help='Routing table input (ip route output) as a string.')
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


def _validate_output(output_elements: list) -> list:
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

    if not output_elements or not any("gateway" in elem for elem in output_elements):
        print(error_message)
        exit(0)

    return output_elements


def generate_output(output: list, classic_printing=True) -> str:
    """
    Generates a string representation of the output list.

    This function either formats the output list as a JSON string or, if classic printing is enabled,
    manually constructs a string representation that mimics a JSON array format by enclosing the list
    in brackets and separating elements with commas. The classic printing mode is intended for scenarios
    where JSON formatting is not preferred or applicable.

    Args:
        output (list): The list of dictionaries representing parsed routing information.
        classic_printing (bool, optional): Flag indicating whether to use classic printing instead of JSON. Defaults to True.

    Returns:
        str: The formatted string representation of the output.
    """
    if classic_printing:
        output.append("]")
        output.insert(0, "[")
        final_output: list = []

        for i, e in enumerate(output):
            if 1 < i < len(output) - 1:
                final_output.append(",")

            final_output.append(e)

        return "".join(str(j) for j in final_output)

    return json.dumps(output, indent=2)


def parse_and_transform() -> None:
    """
    Main function that orchestrates the parsing and printing of routing table information.
    """
    name_of_file: str = "parser_templates/ip_route.template"

    result_from_command_as_a_list_parsed, as_fsm = _parse_input(name_of_file,
                                                                _take_input_directly_from_iproute_command())
    extracted_result = _extract_output(result_from_command_as_a_list_parsed, as_fsm)
    output_with_needed_structure: str = generate_output(_validate_output(extracted_result), classic_printing=True)

    print(output_with_needed_structure)


if __name__ == '__main__':
    parse_and_transform()
