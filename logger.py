import os
from functools import wraps
from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        with open('main.log', 'a') as log_file:
            log_file.write(f"{datetime.now()} ")
            log_file.write(f"Function: {old_function.__name__} ")
            log_file.write(f"Args: {args}, Kwargs: {kwargs} ")
            result = old_function(*args, **kwargs)
            log_file.write(f"Return value: {result}\n")
        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'Файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'Должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
