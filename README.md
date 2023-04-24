# Симплекс-метод

## Формат входных данных

txt-файл следующего содержания:

Указываем иксы, действия с ними (+/-) и что мы ищем (min/max):

```
F=(x1, x2, ...)= x1 + 1x2 -> max
```

Далее, начиная каждую строку с пробела, прописываем ограничения модели:

```
 2x1 + 3x2 <= 1200
```

После системы неравенств, оставив одну строку пустой, можем прописать ожидаемый результат:

```

F=1750
x1=450
x2=100
```

# Запуск

Чтобы запустить программу, в командной строке прописать:

```
py main.py [путь к txt-шнику]
```
