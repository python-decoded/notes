from pydantic import BaseModel, field_validator, ValidationInfo


class MyClass(BaseModel):
    phone: int | None = None
    email: str | None = None

    @field_validator("phone", "email", mode="before")
    @classmethod
    def validate_contact(cls, v, info: ValidationInfo):
        data = {info.field_name: v} | info.data
        print(f"Перевірка поля {info.field_name}")

        if "phone" in data and "email" in data:
            if not data["phone"] and not data["email"]:
                raise ValueError("phone або email треба вказати")
            else:
                print("Перевірка успішна")

        return v


MyClass()
