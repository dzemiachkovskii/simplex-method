import sys
import re
import numpy as np


def main():
    if len(sys.argv) < 2:
        print('Укажите файл с исходными данными!')
        exit(1)
    print(f'Файл: {sys.argv[1]}\n')

    table = get_simplex_table(sys.argv[1])


def get_simplex_table(path):
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

    print(*table, sep='\n\n')

    print(f'max? {searching_max}\n')
    print(f'func = {func}\n')
    print(f'ref plan: {ref_plan}\n')
    print(f'coeffs: {coeffs}\n')
    print(f'restrictions: {restrictions}\n')

    return [['af', 'af'], ['af', 'af']]


if __name__ == '__main__':
    main()
