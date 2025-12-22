from pydantic import BaseModel
from typing import Literal, Union


class PaymentSucceeded(BaseModel):
    id: int
    amount: float
    user_name: str


class UserDeleted(BaseModel):
    user_name: str
    reason: str


class WebhookEnvelope(BaseModel):
    event: Literal["payment.succeeded", "user.deleted"]
    data: Union[PaymentSucceeded, UserDeleted]



def process_request(raw_data: dict):

    envelope = WebhookEnvelope.model_validate(raw_data)

    match envelope:
        case WebhookEnvelope(
            event="payment.succeeded",
            data=PaymentSucceeded() as payment
        ):
            print(f"Payment OK: {payment.user_name=} {payment.amount=}")

        case WebhookEnvelope(
            event="user.deleted",
            data=UserDeleted() as user
        ):
            print(f"User deleted: {user.user_name=} reason={user.reason}")

        case _:
            raise ValueError("Unhandled event")

    return "SUCCESS"


process_request({
    "event": "payment.succeeded",
    "data": {
        "id": 356,
        "amount": 24.5,
        "user_name": "John"
    }
})

process_request({
    "event": "user.deleted",
    "data": {
        "user_name": "John",
        "reason": "fraud"
    }
})
