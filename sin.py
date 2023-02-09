''' This module provides funtions to work with SIN number '''

from typing import List

__author__ = 'Manh Truong Nguyen'
__license__ = 'MIT License'


EVEN_DIGIT_INDEXES = (1, 3, 5, 7)  # Position (2, 4, 6, 8) in SIN number
ODD_DIGIT_INDEXES = (0, 2, 4, 6)  # Position (1, 3, 5, 7) in SIN number


def sum_digits(digits: List[int | str], skip_index=-1) -> int:
    '''
    Sum all digits exept the last from a given list. If a digit is in
    an even position of SIN number,double it and add its digits then continue the sum.

        Parameters:
            digits (List[str]): A list of digits
            skip_index (int): The index of a digit to skip.
                              An index out of the list range means no digit is skipped

        Returns:
            digit_sum (int): The sum of SIN digits
    '''

    digit_sum: int = 0

    for i, digit in enumerate(digits):
        if i != skip_index and i in EVEN_DIGIT_INDEXES:
            doubled: str = str(2 * digit)
            if len(doubled) == 2:
                left: int = int(doubled[0:1])
                right: int = int(doubled[1])
                left_right = left + right
                digit_sum += left_right
            if len(doubled) == 1:
                digit_sum += int(doubled)
        if i != skip_index and i in ODD_DIGIT_INDEXES:
            digit_sum += int(digit)

    return digit_sum


def find_missing_digit(sin: str, index: int) -> int:
    '''
    Find ONE missing digit in a given string of SIN number

        Parameters:
            sin (str): A string of SIN number
            index (int): The index of the missing digit

        Returns:
            missing_digit (int): The missing digit or -1 if can't find any
    '''

    digits: List[int | str] = [int(x) if x.isdigit() else x for x in sin]
    missing_digit: int = -1
    digit_sum: int = 0

    if index == 8:  # Find check digit
        digit_sum = sum_digits(digits)
        missing_digit = - digit_sum % 10

    if index != 8:  # Find main digit
        check_digit: int = int(digits[-1])
        digit_sum = sum_digits(digits, index)

        if index in ODD_DIGIT_INDEXES:
            missing_digit = (- check_digit - digit_sum) % 10
        if index in EVEN_DIGIT_INDEXES:
            doubled_missing_digit = (- check_digit - digit_sum) % 10

            if doubled_missing_digit % 2 == 0:
                missing_digit = int(doubled_missing_digit / 2)
            # This is the case where 2x is congruent to an odd number
            if doubled_missing_digit % 2 != 0:
                missing_digit = int((doubled_missing_digit + 9) / 2)

    return missing_digit
