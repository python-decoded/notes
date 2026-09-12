import threading

# Константи для станів (так само, як у CPython)
PENDING = 'PENDING'
FINISHED = 'FINISHED'


class MyFuture:
    def __init__(self):
        # 1. Створюємо Condition для синхронізації
        self._condition = threading.Condition()
        self._state = PENDING
        self._result = None

    def result(self, timeout=None):
        """Метод для отримання результату. Блокує потік, якщо результат ще не готовий."""
        # 2. Завжди заходимо через лок кондішна
        with self._condition:
            # Чекаємо в циклі while, поки стан є PENDING
            # (wait_for робить під капотом саме такий цикл)
            while self._state == PENDING:
                print(f"⏳ [{threading.current_thread().name}]: Результату немає, засинаю в Condition...")

                # Потік відпускає лок і спить тут, поки його не розбудить notify_all()
                signaled = self._condition.wait(timeout=timeout)

                # Якщо вийшов таймаут, а стан все ще PENDING
                if not signaled and self._state == PENDING:
                    raise TimeoutError("Перевищено час очікування результату!")

            # 3. Коли потік прокинувся і стан змінився на FINISHED, повертаємо значення
            return self._result

    def set_result(self, value):
        """Метод для запису результату. Будить усі потоки, що чекали."""
        with self._condition:
            # Захист від повторного запису (ф'ючер одноразовий)
            if self._state == FINISHED:
                raise RuntimeError("Неможливо записати результат у ф'ючер двічі!")

            print(f"📢 [{threading.current_thread().name}]: Обчислення завершено! Записую значення.")

            # Змінюємо стан та зберігаємо дані
            self._result = value
            self._state = FINISHED

            # 4. СИГНАЛ (Notify All): Будимо абсолютно всі потоки,
            # які «зависли» на методі .result()
            self._condition.notify_all()

    def done(self):
        """Миттєва перевірка стану без блокування"""
        with self._condition:
            return self._state == FINISHED


if __name__ == '__main__':

    future = MyFuture()

    def receiver():
        print("waiting result")
        val = future.result()
        print(f"Значення Фьючера: {val}")

    def provider():
        import time
        time.sleep(5)
        future.set_result(1)


    t1 = threading.Thread(target=receiver)
    t2 = threading.Thread(target=receiver)
    t1.start()
    t2.start()

    t3 = threading.Thread(target=provider)
    t3.start()

    t1.join()
    t2.join()
    t3.join()
