'''
Developed in python 3.11.1
Entry point script for Question 5.
Executes __test__.py for Unit testing with basic cases
'''

from typing import List, Literal, Tuple

import sin
import upc
import isbn

__author__ = 'Manh Truong Nguyen'
__license__ = 'MIT License'


OPTIONS = ('1', '2', '3', 'sin', 'upc', 'isbn')
OPTION_SIN = ('1', 'sin')
OPTION_UPC = ('2', 'upc')
OPTION_ISBN = ('3', 'isbn')

CONTROL_OPTIONS = ('1', '2', 'restart', 'quit')
RESTART_CONTROL_OPTION = ('1', 'restart')
QUIT_CONTROL_OPTION = ('2', 'quit')


def get_missing_digit_index(input_number: str) -> int:
    '''
    Return the index of the missing digit in the input number
    assuming the input number only contains ONE missing digit
    '''
    digits: List[int | str] = [int(x) if x.isdigit() else x for x in input_number]
    result: int = -1
    for i, digit in enumerate(digits):
        if isinstance(digit, str):
            result = i
            break
    return result


def is_valid_number(input_number: str, valid_length: int, is_isbn=False) -> Literal[-2, -1, 0, 1]:
    '''
    Check the validity of the input number in terms of format.
    This function does not check for logical validity.
    Returns 1 if the input number has valid length and 1 missing digit
            0 if the input number has valid length and 0 missing digit
           -1 if the input number has valid length and more than 1 missing digit
           -2 if the input number has invalid length
    '''
    non_digit_count: int = 0
    chars: List[int | str] = [int(x) if x.isdigit() else x for x in input_number]
    for char_index, char in enumerate(chars):
        valid_isbn_x_input = (
            is_isbn and chars[-1] == 'X' and
            char_index != (len(chars) - 1) and not isinstance(char, int))
        valid_isbn_non_x_input = (is_isbn and chars[-1] != 'X' and not isinstance(char, int))
        valid_non_isbn_input = (not is_isbn and not isinstance(char, int))
        if valid_non_isbn_input or valid_isbn_x_input or valid_isbn_non_x_input:
            non_digit_count += 1
    if len(input_number) == valid_length and non_digit_count == 1:
        return 1
    if len(input_number) == valid_length and non_digit_count == 0:
        return 0
    if len(input_number) == valid_length and non_digit_count not in (0, 1):
        return -1
    return -2


def loop_user_selection(options: Tuple, description: str, input_instruction: str, err: str) -> str:
    ''' Loop the input when user is selecting an option. Only breaks when selection is valid '''
    user_input: str = ''
    print(description)
    while True:
        user_input = input(input_instruction).lower()
        if user_input in options:
            break
        print(err)
    return user_input


def loop_number_input(valid_length: int,
                      input_instruction: str,
                      err: str,
                      is_isbn=False,
                      ) -> str:
    ''' Loop the input when user is entering a number. Only breaks if number is valid '''
    user_input: str = ''
    while True:
        user_input = input(input_instruction)
        checked_input: Literal[-2, -1, 0, 1] = is_valid_number(user_input, valid_length, is_isbn)
        if checked_input == -2:
            print(f'{err}: Number has invalid length\n')
        if checked_input == -1:
            print(f'{err}: Number has more than 1 missing digit.\n')
        if checked_input == 0 and is_isbn and user_input[-1] == 'X':
            print(
                f'\n{err}: Number has 0 missing digit.\n'
                f'You have a check digit of 10 (Roman \'X\').\n'
                f'If your intention is to find a check digit, '
                f'use lowercase \'x\' or replace it with another character.\n'
            )
        if checked_input == 0 and not is_isbn:
            print(f'{err}: Number has 0 missing digit.\n')
        if checked_input == 1:
            break
    return user_input


def main(user_selection: str, number: str, missing_digit: int | str):
    ''' Main function of application '''
    user_selection = loop_user_selection(OPTIONS,
                                         '\n\n1. SIN\t\t2. UPC\t\t3. ISBN',
                                         'Enter [1-3] or a type of number to continue: ',
                                         'Invalid selection')

    if user_selection in OPTION_SIN:
        number = loop_number_input(
            9,
            'Enter a 9-digit SIN number with 1 any-non-digit character: ', 'Invalid SIN format'
        )
        missing_digit_index = get_missing_digit_index(number)
        missing_digit = sin.find_missing_digit(number, missing_digit_index)
        if missing_digit_index == 8:
            print(
                f'The missing check digit of SIN {number} '
                f'is {"COULD NOT BE FOUND" if missing_digit == -1 else missing_digit}'
            )
        if missing_digit_index != 8:
            order_abbreviation = ("st" if missing_digit_index ==
                                  0 else "nd" if missing_digit_index == 1 else "th")
            print(
                f'The missing {missing_digit_index+ 1}{order_abbreviation} digit of UPC {number} '
                f'is {"COULD NOT BE FOUND" if missing_digit == -1 else missing_digit}'
            )

    if user_selection in OPTION_UPC:
        number = loop_number_input(
            12,
            'Enter a 12-digit UPC number with 1 any-non-digit character: ', 'Invalid UPC format'
        )
        missing_digit_index = get_missing_digit_index(number)
        missing_digit = upc.find_missing_digit(number, missing_digit_index)
        if missing_digit_index == 11:
            print(
                f'The missing check digit of UPC {number} '
                f'is {"COULD NOT BE FOUND" if missing_digit == -1 else missing_digit}'
            )
        if missing_digit_index != 11:
            order_abbreviation = ("st" if missing_digit_index ==
                                  0 else "nd" if missing_digit_index == 1 else "th")
            print(
                f'The missing {missing_digit_index+ 1}{order_abbreviation} digit of UPC {number} '
                f'is {"COULD NOT BE FOUND" if missing_digit == -1 else missing_digit}'
            )

    if user_selection in OPTION_ISBN:
        number = loop_number_input(
            10,
            'Enter a 10-digit ISBN number with 1 any-non-digit character\n' +
            'Use Roman numeral \'X\' (capitalized) for check digit of 10: ',
            'Invalid ISBN format',
            True,
        )
        missing_digit_index = get_missing_digit_index(number)
        missing_digit = isbn.find_missing_digit(number, missing_digit_index)
        if missing_digit_index == 9:
            print(
                f'The missing check digit of ISBN {number} '
                f'is {"COULD NOT BE FOUND" if missing_digit == -1 else missing_digit}'
            )
        if missing_digit_index != 9:
            order_abbreviation = ("st" if missing_digit_index ==
                                  0 else "nd" if missing_digit_index == 1 else "th")
            print(
                f'The missing {missing_digit_index + 1}{order_abbreviation} digit of ISBN {number} '
                f'is {"COULD NOT BE FOUND" if missing_digit == -1 else missing_digit}'
            )


# Script starts from here
if __name__ == '__main__':
    user_control: str = ''
    selection: str = ''
    num: str = ''
    missing_dig: int | str = -1

    try:
        while True:
            main(selection, num, missing_dig)

            while True:
                print('\n\n1. Restart\t2. Quit')
                user_control = input(
                    'Choose an option [1-2] or type in the option to continue: '
                ).lower()
                if user_control in CONTROL_OPTIONS:
                    break
                print('Invalid selection')

            if user_control in RESTART_CONTROL_OPTION:
                pass

            if user_control in QUIT_CONTROL_OPTION:
                break
    except KeyboardInterrupt as e:
        print('\nBye')
