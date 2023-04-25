import sys
import re
import numpy as np


def main():
    if len(sys.argv) < 2:
        print('Укажите файл с исходными данными!')
        exit(1)
    print(f'Файл: {sys.argv[1]}\n')

    table, searching_max, expected_results = get_simplex_table(sys.argv[1])

    for i in table:
        for j in i:
            print(int(j), end='\t')
        print()


def get_simplex_table(path):
    """
    Returns
    1) Simplex table (numpy array);
    2) Boolean, indicating whether we are looking for the maximum or minimum;
    3) Expected result, if passed;
    """
    with open(path, 'r') as f:
        func = f.readline()[:-1]
        restrictions = []
        for line in f:
            if line == '\n':
                break
            restrictions.append(line[:-1])
        results = f.readlines()

    searching_max = 'max' in func

    func = func[func.find('=') + 1:func.find('->')]  # stripping from redundant data
    func = func.replace(' x', ' 1x')  # same
    func = func.replace(' -x', ' -1x')  # same
    func = func.replace(' ', '')  # same
    func = re.findall(r'-*\d+x\d+', func)  # searching for all -9x9-like substrings
    func = [coeff[:coeff.find('x')] for coeff in func]  # extracting coefficients from arguments
    func = [-int(arg) for arg in func]  # reversing all elements & casting them to integers

    ref_plan = ['0'] * len(func)
    for restriction in restrictions[:-1]:
        ref_plan.append(restriction[restriction.find('=') + 2:])

    coeffs = []
    for i, line in enumerate(restrictions[:-1]):
        line = line.replace(' x', ' 1x')  # stripping from redundant data
        line = line.replace(' -x', ' -1x')
        line = line.replace(' ', '')
        line = re.findall(r'-*\d+x\d+', line)  # searching for all -9x9-like substrings
        line = [coeff[:coeff.find('x')] for coeff in line]  # extracting raw numbers from argument
        artificial_variables = [0] * (len(restrictions) - 1)
        artificial_variables[i] = 1
        line += artificial_variables
        coeffs.append(line)

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


if __name__ == '__main__':
    main()
