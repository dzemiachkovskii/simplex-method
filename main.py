import sys


def main():
    if len(sys.argv) < 2:
        print('Укажите файл с исходными данными!')
        return
    print(f'Файл: {sys.argv[1]}')
