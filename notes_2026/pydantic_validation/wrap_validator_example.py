from typing import Annotated
from pydantic import BaseModel, Field, WrapValidator, ValidatorFunctionWrapHandler


def processor(data: list | str, handler: ValidatorFunctionWrapHandler) -> list:

    # Початкова Обробка
    if isinstance(data, str):
        data = data.split(",")

    # Вбудована Перевірка
    data = handler(data)

    # Додаткові Перевірки
    if len(data) == 0:
        raise ValueError("Колекція не може бути пустою")

    return data


class MyClass(BaseModel):
    tags: Annotated[list, WrapValidator(processor)] = Field(default_factory=list)


obj = MyClass(tags="tag1,tag2,tag3")

for tag in obj.tags:
    print(tag)
