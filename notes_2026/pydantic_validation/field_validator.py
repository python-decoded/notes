from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class MyClass(BaseModel):
    birth_date: datetime
    tags: list = Field(default_factory=list)

    @field_validator("birth_date", mode="after")
    @classmethod
    def check_18_plus(cls, v: datetime) -> datetime:
        today = datetime.today()
        # чи був уже день народження цього року
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))

        if age < 18:
            raise ValueError("Вам має бути не менше 18 років")
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def csv_to_list(cls, data: list | str) -> list:
        if isinstance(data, str):
            data = data.split(",")
        return data


obj = MyClass(birth_date="2000-04-25", tags="tag1,tag2,tag3")


for tag in obj.tags:
    print(tag)
