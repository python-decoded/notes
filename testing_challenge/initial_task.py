"""
Покрийте тестами запропоновані функції
Не забувайте використовувати техніки тест дизайну

Очікувана структура проекту:

+ tasks
  |_ __init__.py
  |_ not_reliable_function_1.py
  |_ not_reliable_function_2.py
  |_ retry_tool.py
  |_ get_connection.py

+ tests
  |_ __init__.py
  |_ test_not_reliable_function_1.py
  |_ test_not_reliable_function_2.py
  |_ test_retry_tool.py
  |_ test_get_connection.py


Очікується, що жодні зміни не будуть внесені у файли у папці tasks
"""

# ----------- tasks/not_reliable_function_1.py ------------------

"""
В цьому випадку random.choice є ненадійним компонентом
адже результат його роботи непередбачуваний.
Потрібно написати надійні тести
які б перевіряли логіку роботи функції not_reliable

Важливо перевірити як positive так і negative сценарії
"""

import random


def not_reliable():
    data = random.choice(range(10))
    if data < 5:
        raise ValueError
    return data


# ---------------- tasks/not_reliable_function_2.py ------------------

"""
Задача схожа на попередню, 
але імпорт та використання функції choice виконаний трохи поіншому
"""

from random import choice


def not_reliable():
    data = choice(range(10))
    if data < 5:
        raise ValueError
    return data


# -------------   tasks/retry_tool.py --------------
"""
Необхідно протестувати декоратор,
який дозволяє робити повторні виклики у задекоровану фукнцію
у випадку якщо сталася помилка при її виклику.
"""


def retry(times: int = 0):
    """
    Параметризований декоратор,
    дозволяє зробити повторний виклик задекорованої функції
    якщо при її виклику сталася помилка,

    :param times: дозволяє вказати кількість очікуваних повторів,
                  по замовчуванню необмежена кількість повторів
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            _times = times

            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    _times -= 1
                    if _times == 0:
                        raise e

        return wrapper

    return decorator


# Приклад використання
# у вашому випадку, потрібно протестувати саме декоратор,
# ви можете створити власну функцію безпосередньо у тесті
# і задекорувати її декоратором.

if __name__ == '__main__':

    from random import choice


    @retry()
    def not_reliable():
        data = choice(range(10))
        if data < 5:
            raise ValueError
        return data


    print(not_reliable())


    @retry(times=2)
    def not_reliable():
        data = choice(range(10))
        if data < 5:
            raise ValueError
        return data


    print(not_reliable())

# -------------------     tasks/get_connection.py    ------------------


"""
В даному прикладі ми очікуємо змінні оточення USER та PASSWORD
але вони можуть бути і не встановлені при локальному запуску тестів

та функцію get_connection всеодно треба якось протестувати
"""

import os

USER = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']


def get_connection():
    if USER and PASSWORD:
        print("Connection is successful")
        return

    raise ConnectionError
