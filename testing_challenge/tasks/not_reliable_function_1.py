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
