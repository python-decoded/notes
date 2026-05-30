from pydantic import BaseModel, field_validator, ValidationInfo


class MyClass(BaseModel):
    phone: int | None = None
    email: str | None = None

    @field_validator("phone", "email", mode="before")
    @classmethod
    def validate_contact(cls, v, info: ValidationInfo) -> str | None:

        return v


MyClass(phone="380631234567", email="foo@com")
