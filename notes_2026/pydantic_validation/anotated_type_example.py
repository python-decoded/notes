from datetime import datetime
from pydantic import BaseModel, Field, AfterValidator

import annotated_types
from typing import Annotated
PositiveInt = Annotated[int, Field(gt=0, le=100, multiple_of=5)]


def check_18_plus(v: datetime) -> datetime:
    today = datetime.today()
    # чи був уже день народження цього року
    age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))

    if age < 18:
        raise ValueError("Вам має бути не менше 18 років")
    return v


class MyClass(BaseModel):
    value: PositiveInt
    birth_date: Annotated[datetime, AfterValidator(check_18_plus)]


MyClass(value=10, birth_date="2016-04-25")
