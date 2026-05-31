from pydantic import BaseModel, field_validator, ValidationInfo, model_validator, ModelWrapValidatorHandler


class MyClass(BaseModel):
    phone: int | None = None
    email: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_contacts_before_mode(cls, data):
        if not data.get("phone") and not data.get("email"):
            raise ValueError("phone або email повинен бути вказаний.")

        return data

    @model_validator(mode="wrap")
    @classmethod
    def validate_contacts_wrap_mode(cls, data, handler: ModelWrapValidatorHandler):
        if not data.get("phone") and not data.get("email"):
            raise ValueError("phone або email повинен бути вказаний.")

        data = handler(data)

        # Робимо щось після вбудованої валідації моделі

        return data

    @model_validator(mode="after")
    def validate_contacts_after_mode(self):
        if not self.phone and not self.email:
            raise ValueError("phone або email повинен бути вказаний.")

        return self


MyClass(phone="380631234567", email="email@gmail.com")
