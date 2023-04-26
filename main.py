import sys
import re
import numpy as np


def main():
    if len(sys.argv) < 2:
        print('Укажите файл с исходными данными!')
        exit(1)
    print('\nСИМПЛЕКС-МЕТОД ДЛЯ ДВУХ ПЕРЕМЕННЫХ')

    table, searching_max, expected_results = get_simplex_table(sys.argv[1])
    simplex_method(table, searching_max)


def get_simplex_table(path):
    """
    Returns
    1) Simplex table (numpy array);
    2) Boolean, indicating whether we are looking for the maximum or minimum;
    3) Expected result, if passed;
    """
    print(f'Файл с исходными данными: {path}\n')
    with open(path, 'r') as f:  # reading from file
        func = f.readline()[:-1]
        restrictions = []
        for line in f:
            if line == '\n':
                break
            restrictions.append(line[:-1])
        results = f.readlines()

    searching_max = 'max' in func.lower()

    func = func[func.find('=') + 1:func.find('->')]  # stripping from redundant data
    func = re.findall(r'-? ?\d*x', func)  # -x or 5x etc
    for i, arg in enumerate(func):
        arg = arg.replace(' ', '')
        if re.match(r'^-?x$', arg):  # swapping x with 1 or void
            func[i] = arg.replace('x', '1')
        else:
            func[i] = arg.replace('x', '')
    func = [-int(arg) for arg in func]  # reversing all elements & casting them to integers

    ref_plan = ['0'] * len(func)
    for restriction in restrictions[:-1]:
        ref_plan.append(restriction[restriction.find('=') + 2:])

    coeffs = []
    for i, line in enumerate(restrictions[:-1]):
        relation = re.findall(r'[</>]=?', line)  # >= or <=
        arguments = re.findall(r'-? ?\d*x', line)  # -x or 5x etc
        for j, arg in enumerate(arguments):
            arg = arg.replace(' ', '')  # removing spaces
            if re.match(r'^-?x$', arg):
                arg = arg.replace('x', '1')
            else:
                arg = arg.replace('x', '')
            arguments[j] = int(arg)
        artificial_variables = [0] * (len(restrictions) - 1)
        artificial_variables[i] = 1 if '<' in str(relation) else -1
        arguments += artificial_variables
        coeffs.append(arguments)

    table = np.empty(shape=(len(coeffs) + 1, len(coeffs[0]) + 1))
    table.fill(0)

    # filling all rows except the last one
    first_col = ref_plan[len(func):]
    for i in range(len(coeffs)):
        line = [first_col[i]] + coeffs[i]
        for j in range(len(table[i])):
            table[i][j] = int(line[j])
    # filling the last row
    for i in range(len(func)):
        table[-1][i + 1] = func[i]

    return table, searching_max, results


def simplex_method(table: np.ndarray, searching_max):
    print('ИЩЕМ ' + ('МАКСИМУМ' if searching_max else 'МИНИМУМ'))
    print('\nСоставим симплекс-таблицу:')
    draw_table(table)
    iteration = 0
    basis = [f'x{i + 3}' for i in range(len(table) - 1)] + ['F']  # ['x3', 'x4', 'x5', 'F'] etc
    print(basis)
    while True:
        if not check_stop(table[-1], searching_max):
            break
    print_results(table)


def draw_table(table):
    width = 16
    header = ['Базис', 'План'] + [f'x{i}' for i in range(1, len(table[0] + 1))] + ['Оц. столбец']
    sep = '\n' + '=' * width * len(header)

    print(sep[1:])
    for el in header:
        print(f'| {el: <{width - 4}} |', end='')
    print(sep)
    for i, row in enumerate(table):
        line_name = 'F' if i == len(table[0]) - 3 else f'x{i + 3}'
        line = (line_name, *row, '')
        for el in line:
            print(f'| {el: <{width - 4}} |', end='')
        print(sep)


def check_stop(row, searching_max):
    satisfies = (lambda x: x >= 0) if searching_max else (lambda x: x <= 0)
    for el in row:
        if not satisfies(el):
            return False
    return True


def print_results(table):
    x1 = table[0][0]
    x2 = table[1][0]
    func = table[3][0]
    print(f'РЕЗУЛЬТАТ:\nF = {func}\nx1 = {x1}\nx2 = {x2}')


if __name__ == '__main__':
    main()
