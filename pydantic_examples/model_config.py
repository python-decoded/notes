from pydantic import BaseModel, Field, ConfigDict


class BaseClass(BaseModel):

    model_config = ConfigDict(populate_by_name=True,
                              validate_by_name=True,  # pydantic 2.11+
                              frozen=True,
                              strict=True,
                              str_strip_whitespace=True,
                              use_enum_values=True,
                              extra="allow")  # allow, forbid


class MyClass(BaseClass):

    first_field: str = Field(validation_alias="firstField")
    second_field: str = Field(validation_alias="secondField")


obj1 = MyClass(firstField="1", secondField="2", foo=123)

print(f"{obj1=}")

print(obj1.first_field)
print(obj1.foo)
print(obj1.model_dump())
print(obj1.model_dump(by_alias=True))

print(MyClass(first_field="1", second_field="2"))
