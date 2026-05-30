from typing import Annotated
from datetime import datetime

from pydantic import BaseModel, Field, AfterValidator, BeforeValidator


def check_18_plus(v: datetime) -> datetime:
    today = datetime.today()
    # чи був уже день народження цього року
    age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))

    if age < 18:
        raise ValueError("Вам має бути не менше 18 років")
    return v


def csv_to_list(data: list | str) -> list:
    if isinstance(data, str):
        data = data.split(",")
    return data


class MyClass(BaseModel):
    birth_date: Annotated[datetime, AfterValidator(check_18_plus)]
    tags: Annotated[list, BeforeValidator(csv_to_list)] = Field(default_factory=list)


obj = MyClass(birth_date="2000-04-25", tags="tag1,tag2,tag3")

for tag in obj.tags:
    print(tag)
