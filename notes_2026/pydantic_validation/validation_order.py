from typing import Annotated
from pydantic import (BaseModel, BeforeValidator,
                      AfterValidator, WrapValidator,
                      ValidatorFunctionWrapHandler, ValidationInfo,
                      field_validator, model_validator, ModelWrapValidatorHandler)


def wrapper(validator, wrap=False):
    def func(v, info: ValidationInfo):
        print(f"       ------ {info.field_name} {validator}")
        return v

    def wrap_func(v, handler: ValidatorFunctionWrapHandler, info: ValidationInfo):
        print(f"       ------ {info.field_name} {validator} start")
        v = handler(v)
        print(f"       ------ {info.field_name} {validator} end")
        return v

    return wrap_func if wrap else func


class MyClass(BaseModel):
    attr1: Annotated[str,
                     BeforeValidator(wrapper("BeforeValidator_1")),
                     BeforeValidator(wrapper("BeforeValidator_2")),
                     AfterValidator(wrapper("AfterValidator_1")),
                     AfterValidator(wrapper("AfterValidator_2")),
                     WrapValidator(wrapper("WrapValidator_1", True)),
                     WrapValidator(wrapper("WrapValidator_2", True)),
                     ] = "attr1"
    attr2: Annotated[str,
                     WrapValidator(wrapper("WrapValidator_1", True)),
                     WrapValidator(wrapper("WrapValidator_2", True)),
                     BeforeValidator(wrapper("BeforeValidator_1")),
                     BeforeValidator(wrapper("BeforeValidator_2")),
                     AfterValidator(wrapper("AfterValidator_1")),
                     AfterValidator(wrapper("AfterValidator_2"))] = "attr2"

    @field_validator("attr1", "attr2", mode="before")
    @classmethod
    def field_validator_before_1(cls, v, info: ValidationInfo):
        print(f"------ {info.field_name} field_validator_1 'before'")
        return v

    @field_validator("attr1", "attr2", mode="before")
    @classmethod
    def field_validator_before_2(cls, v, info: ValidationInfo):
        print(f"------ {info.field_name} field_validator_2 'before'")
        return v

    @field_validator("attr1", "attr2", mode="after")
    @classmethod
    def field_validator_after_1(cls, v, info: ValidationInfo):
        print(f"------ {info.field_name} field_validator_1 'after'")
        return v

    @field_validator("attr1", "attr2", mode="after")
    @classmethod
    def field_validator_after_2(cls, v, info: ValidationInfo):
        print(f"------ {info.field_name} field_validator_2 'after'")
        return v

    @field_validator("attr1", "attr2", mode="wrap")
    @classmethod
    def field_validator_wrap_1(cls, v, handler: ValidatorFunctionWrapHandler, info: ValidationInfo):
        print(f"------ {info.field_name} field_validator_1 'wrap' start")
        v = handler(v)
        print(f"------ {info.field_name} field_validator_1 'wrap' end")
        return v

    @field_validator("attr1", "attr2", mode="wrap")
    @classmethod
    def field_validator_wrap_2(cls, v, handler: ValidatorFunctionWrapHandler, info: ValidationInfo):
        print(f"------ {info.field_name} field_validator_2 'wrap' start")
        v = handler(v)
        print(f"------ {info.field_name} field_validator_2 'wrap' end")
        return v

    # ================= model validators ==============================

    @model_validator(mode="after")
    def model_validator_after_1(self):
        print(f"model_validator_1 'after'")
        return self

    @model_validator(mode="after")
    def model_validator_after_2(self):
        print(f"model_validator_2 'after'")
        return self

    @model_validator(mode="before")
    @classmethod
    def model_validator_before_1(cls, v):
        print(f"model_validator_1 'before'")
        return v

    @model_validator(mode="before")
    @classmethod
    def model_validator_before_2(cls, v):
        print(f"model_validator_2 'before'")
        return v

    @model_validator(mode="wrap")
    @classmethod
    def model_validator_wrap_1(cls, v, handler: ModelWrapValidatorHandler):
        print(f"model_validator_1 'wrap' start")
        v = handler(v)
        print(f"model_validator_1 'wrap' end")
        return v

    @model_validator(mode="wrap")
    @classmethod
    def model_validator_wrap_2(cls, v, handler: ModelWrapValidatorHandler):
        print(f"model_validator_2 'wrap' start")
        v = handler(v)
        print(f"model_validator_2 'wrap' end")
        return v


obj = MyClass(attr1="attr1", attr2="attr2")
