''' This module provides functions to work with ISBN numbers '''

from typing import List

__author__ = 'Manh Truong Nguyen'
__license__ = 'MIT License'

# Position (2, 4, 6, 8, 10) in ISBN number
EVEN_DIGIT_INDEXES = (1, 3, 5, 7, 9)
ODD_DIGIT_INDEXES = (0, 2, 4, 6, 8)  # Position (1, 3, 5, 7, 9) in ISBN number


def sum_digits(digits: List[int | str], skip_index: int = -1) -> int:
    '''
    Sum all digits except the last and the one at skip_index from a given list. From left to right, 
    the digits are multiplied by incrementing multipliers starting from 1 before adding together

        Parameters:
            digits (List[str]): A list of digits
            skip_index (int): The index of a digit to skip.
                              An index out of the list range means no digit is skipped

        Returns:
            digit_sum (int): The sum of ISBN multiplied digits
    '''
    digit_sum: int = 0
    for i, digit in enumerate(digits):
        # Skip check digit, missing digit, and assert type
        if i not in (skip_index, 9) and isinstance(digit, int):
            digit_sum += digit * (i + 1)
    return digit_sum


def find_missing_digit(upc: str, index: int) -> int | str:
    '''
    Find ONE missing digit in a given string of UPC number

        Parameters:
            upc (str): A string of UPC number with 1 missing digit
            index (int): The index of the missing digit

        Returns:
            missing_digit (int): The missing digit or -1 if can't find any after certain loop cycles
    '''

    # Split the UPC string into single digits in a list
    digits: List[int | str] = [int(x) if x.isdigit() else x for x in upc]
    has_check_digit_x = digits[-1] == 'X'
    missing_digit: int | str = -2
    digit_sum: int = 0

    if index == 9:  # Find check digit
        digit_sum = sum_digits(digits)
        missing_digit = digit_sum % 11
        if digit_sum % 11 == 10:
            missing_digit = '\'X\' (as 10)'

    if index != 9:  # Find main digit
        digit_sum = sum_digits(digits, index)
        position: int = index + 1
        check_digit: int = 10 if has_check_digit_x else int(digits[-1])
        multiplied_missing_digit: int = (check_digit - digit_sum) % 11

        loop_cycles: int = 0
        while loop_cycles < 5000:
            if multiplied_missing_digit % position == 0:
                missing_digit = int(
                    multiplied_missing_digit / position
                )  # cast integer because division returns float
                break
            if multiplied_missing_digit % position != 0:
                multiplied_missing_digit += 11
                loop_cycles += 1

    return missing_digit
