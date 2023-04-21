import sys

if len(sys.argv) < 2:
    print('Укажите файл с исходными данными!')
    exit(1)
print(f'Файл: {sys.argv[1]}')
