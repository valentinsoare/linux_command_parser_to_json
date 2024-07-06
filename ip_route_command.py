#!/usr/bin/python3

import argparse
import textfsm


def _take_input() -> str:
    parser = argparse.ArgumentParser(description='Parse linux routing table output.')
    parser.add_argument('input_string', type=str, help='Routing table input (ip route output) as a string.')
    args = parser.parse_args()

    return args.input_string


def _take_input_mock() -> str:
    input_from_user: str = """
default via 192.168.100.1 dev enp52s0 proto dhcp src 192.168.100.35 metric 100
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
192.168.100.0/24 dev enp52s0 proto kernel scope link src 192.168.100.35 metric 100
"""
    return input_from_user


def _parse_input(name_of_file_template: str, input_from_user: str) -> tuple:
    with open(name_of_file_template) as template_file:
        fsm = textfsm.TextFSM(template_file)
        parsed_results = fsm.ParseText(input_from_user)

    return parsed_results, fsm


def _extract_output(content_parsed: list, fsm_like: object) -> list:
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
    for i in range(len(output)):
        if (i > 0) and (i < (len(output) - 2)):
            print(output[i], end=",")
        else:
            print(output[i], end="")


def main():
    name_of_file: str = "parser_templates/ip_route.template"

    result_from_command_as_a_list_parsed, as_fsm = _parse_input(name_of_file, _take_input_mock())
    extracted_result = _extract_output(result_from_command_as_a_list_parsed, as_fsm)
    _print_the_output(extracted_result)


if __name__ == '__main__':
    main()
