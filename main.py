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

    func = func[func.find('=') + 1:func.find('->')].replace(' ', '')
    func = re.findall(r'-*[0-9]*x[0-9]+', func)
    func = [arg[:arg.find('x')] for arg in func]
    func = [arg if re.match(r'[0-9]+', arg) else arg + '1' for arg in func]

    print(searching_max, func, restrictions, results, sep='\n\n')

    return [['af', 'af'], ['af', 'af']]


if __name__ == '__main__':
    main()
