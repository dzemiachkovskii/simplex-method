import sys
import re
import numpy as np


def main():
    if len(sys.argv) < 2:
        print('Укажите файл с исходными данными!')
        exit(1)
    print('\nСИМПЛЕКС-МЕТОД ДЛЯ ДВУХ ПЕРЕМЕННЫХ')

    table, searching_max, expected_results = get_simplex_table(sys.argv[1])
    results = simplex_method(table, searching_max)
    print(f'Результат работы программы:\n{results}\n')
    print(f'Ожидаемый результат:\n{expected_results}')


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

    results = '\n'.join([el.strip().replace('\n', '') for el in results])

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

    iteration = 0
    basis = [f'x{i + 3}' for i in range(len(table) - 1)] + ['F']  # ['x3', 'x4', 'x5', 'F'] etc`
    draw_table(basis, table, iteration)
    while True:
        if check_stop(table[-1], searching_max):
            break
        if iteration > 5:
            print('Больше 5 итераций. Возможно, всё сломалось...')
        try:
            pivot, pivot_i, pivot_j = get_pivot(table, searching_max)
        except ValueError:
            return 'Функция стремится к ' + ('+∞' if searching_max else '-∞')
        basis[pivot_i] = f'x{pivot_j}'
        new_table = np.copy(table)

        for j in range(len(new_table[pivot_i])):  # dividing all elements in pivot row by pivot
            new_table[pivot_i][j] /= pivot

        for i in range(len(table)):
            if i == pivot_i:  # skipping pivot row
                continue
            for j in range(len(table[i])):
                if j == pivot_j:
                    new_table[i][j] = 0  # if element is in the pivot column — assign it to zero
                else:
                    matrix = [
                        [table[i][j], table[i][pivot_j]],
                        [table[pivot_i][j], table[pivot_i][pivot_j]]
                    ]

                    new_table[i][j] = ((matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])) / pivot
        table = new_table
        iteration += 1
        draw_table(basis, table, iteration)
    x1 = table[
        basis.index('x1')
    ][0]
    x2 = table[
        basis.index('x2')
    ][0]
    func = table[-1][0]
    return f'F = {func}\nx1 = {x1}\nx2 = {x2}'


def draw_table(basis, table, iteration):
    width = 16
    header = ['Базис', 'План'] + [f'x{i}' for i in range(1, len(table[0] + 1))]
    sep = '\n' + '=' * width * len(header)
    basis = basis[::-1]

    print(sep)
    print(f'{iteration}-я итерация')
    print(sep[1:])
    for el in header:
        print(f'| {el: <{width - 4}} |', end='')
    print(sep)
    for i, row in enumerate(table):
        line_name = basis.pop()
        line = (line_name, *row)
        for el in line:
            if type(el) is not str:
                el = round(el, 5)
            print(f'| {el: <{width - 4}} |', end='')
        print(sep)


def check_stop(row, searching_max):
    satisfies = (lambda x: x >= -0) if searching_max else (lambda x: x <= 0)
    for el in row:
        if not satisfies(el):
            return False
    return True


def get_pivot(table, searching_max):
    pivot_i = 0
    pivot_j = 0
    el_in_func_row = min(table[-1]) if searching_max else max(table[-1])  # finding pivot column
    for j, el in enumerate(table[-1]):
        if el == el_in_func_row:
            pivot_j = j
            break
    eval_column = [table[i][0] / table[i][pivot_j] if table[i][pivot_j] > 0 else 999999999999999999 for i in
                   range(len(table) - 1)]  # creating evaluation column
    if all(el == 999999999999999999 for el in eval_column):
        raise ValueError('no pivot')
    min_el_in_eval_col = max(eval_column)
    for i, el in enumerate(eval_column):  # finding pivot row
        if el < abs(min_el_in_eval_col):
            min_el_in_eval_col = el
            pivot_i = i
    pivot = table[pivot_i][pivot_j]
    print(f'Разрешающий элемент с индексами [{pivot_i}][{pivot_j}] = {round(pivot, 5)}')
    return pivot, pivot_i, pivot_j


if __name__ == '__main__':
    main()
