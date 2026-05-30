from typing import Annotated
from pydantic import BaseModel, Field
import annotated_types


PositiveInt = Annotated[int,
                        annotated_types.Gt(0),
                        annotated_types.Le(100),
                        annotated_types.MultipleOf(5)]

PositiveInt = Annotated[int,
                        Field(gt=0, le=100, multiple_of=5)]


class MyClass(BaseModel):
    a: PositiveInt


a = MyClass(a=17)
