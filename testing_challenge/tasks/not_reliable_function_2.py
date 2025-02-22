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
