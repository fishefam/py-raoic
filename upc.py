''' This module provides functions to work with UPC codes '''

from typing import List

__author__ = 'Manh Truong Nguyen'
__license__ = 'MIT License'


EVEN_DIGIT_INDEXES = (1, 3, 5, 7, 9, 11)  # Position (2, 4, 6, 8, 10, 12) in UPC code
ODD_DIGIT_INDEXES = (0, 2, 4, 6, 8, 10)  # Position (1, 3, 5, 7, 9, 11) in UPC code


def sum_digits(digits: List[int | str], skip_index=-1) -> int:
    '''
    Sum all digits except the last and the one at skip_index from a given list.
    If a digit is in an odd position of UPC code, thriple it and continue the sum.

        Parameters:
            digits (List[str]): A list of digits
            skip_index (int): The index of a digit to skip.
                              An index out of the list range means no digit is skipped

        Returns:
            digit_sum (int): The sum of UPC digits
    '''

    digit_sum: int = 0

    for i, digit in enumerate(digits):
        if i not in (skip_index, 11) and isinstance(digit, int) and i in ODD_DIGIT_INDEXES:
            digit_sum += 3 * digit
        if i not in (skip_index, 11) and isinstance(digit, int) and i in EVEN_DIGIT_INDEXES:
            digit_sum += digit

    return digit_sum


def find_missing_digit(upc: str, index: int) -> int:
    '''
    Find ONE missing digit in a given string of UPC number

        Parameters:
            upc (str): A string of UPC number
            index (int): The index of the missing digit

        Returns:
            missing_digit (int): The missing digit or -1 if can't find any after certain loop cycles
    '''

    digits: List[int | str] = [int(x) if x.isdigit() else x for x in upc]
    missing_digit: int = -1
    digit_sum: int = 0

    if index == 11:  # Find check digit
        digit_sum = sum_digits(digits)
        missing_digit = - digit_sum % 10

    if index != 11:  # Find main digit
        check_digit: int = int(digits[-1])
        digit_sum = sum_digits(digits, index)

        if index in EVEN_DIGIT_INDEXES:
            missing_digit = (- check_digit - digit_sum) % 10
        if index in ODD_DIGIT_INDEXES:
            thripled_missing_digit = (- check_digit - digit_sum) % 10

            loop_cycles: int = 0
            while loop_cycles < 5000:
                if thripled_missing_digit % 3 == 0:
                    missing_digit = int(thripled_missing_digit / 3)
                    break
                if thripled_missing_digit % 3 != 0:
                    thripled_missing_digit += 10
                    loop_cycles += 1

    return missing_digit
