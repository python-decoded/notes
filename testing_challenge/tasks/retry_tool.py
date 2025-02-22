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
