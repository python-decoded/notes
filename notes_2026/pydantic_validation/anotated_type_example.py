from pydantic import BaseModel, Field

import annotated_types
from typing import Annotated
PositiveInt = Annotated[int, Field(gt=0, le=100, multiple_of=5)]


class MyClass(BaseModel):
    value: PositiveInt


MyClass(value=17)
