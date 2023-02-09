''' Basic unit tests for sin, upc, isbn modules '''

from typing import List, Tuple
import sin
import upc
import isbn

# Test cases of known valid numbers
SINS = ('732482047', '428804108', '744762741')
UPCS = ('639382000393', '883028594054', '042100005264')
ISBNS = ('1603094989', '1603095136', '1603095543', '091889428X')


def generate_number_with_missing_digit(number: str) -> List[Tuple[str, int | str, int]]:
    ''' Prepare testing items '''
    result: List[Tuple[str, int | str, int]] = []
    for i, digit in enumerate(number):
        number_with_missing_digit: str = f'{number[0:i]}x{number[i+1:]}' if i < len(
            number) - 1 else f'{number[0:i]}x'
        tup: Tuple[str, int | str, int] = (number_with_missing_digit,
                                           "'X' (as 10)" if digit == 'X' else int(digit), i)
        result.append(tup)
    return result


def flatten(main_list: List[List]) -> List:
    ''' Flatten a 2-D list down to 1 level '''
    return [item for sublist in main_list for item in sublist]


if __name__ == '__main__':
    # SIN unit test
    print('================== Testing SIN module ==================')
    sin_tests = flatten([generate_number_with_missing_digit(x) for x in SINS])
    for i_sin, sin_test in enumerate(sin_tests):
        missing_digit: int | str = sin.find_missing_digit(sin_test[0], sin_test[2])
        if missing_digit == sin_test[1]:
            print(f'Passed test {i_sin + 1}')
        if missing_digit != sin_test[1]:
            print(f'Failed test {i_sin + 1}')
    print('================== Finished testing SIN module ==================\n\n')

    # UPC unit test
    print('================== Testing UPC module ==================')
    upc_tests = flatten([generate_number_with_missing_digit(x) for x in UPCS])
    for i_upc, upc_test in enumerate(upc_tests):
        missing_digit = upc.find_missing_digit(upc_test[0], upc_test[2])
        if missing_digit == upc_test[1]:
            print(f'Passed test {i_upc + 1}')
        if missing_digit != upc_test[1]:
            print(f'Failed test {i_upc + 1}')
    print('================== Finished testing UPC module ==================\n\n')

    # ISBN unit test
    print('================== Testing ISBN module ==================')
    isbn_tests = flatten([generate_number_with_missing_digit(x) for x in ISBNS])
    for i_isbn, isbn_test in enumerate(isbn_tests):
        missing_digit = isbn.find_missing_digit(isbn_test[0], isbn_test[2])
        if missing_digit == isbn_test[1]:
            print(f'Passed test {i_isbn + 1}')
        if missing_digit != isbn_test[1]:
            print(f'Failed test {i_isbn + 1}')
    print('================== Finished testing ISBN module ==================')
