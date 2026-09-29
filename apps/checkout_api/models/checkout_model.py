from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, ConfigDict


class CheckoutRequestModel(BaseModel):
    subtotal: Decimal
    tax_rate: Decimal
    user_id: str

    # Shows example of the request model in the FastAPI docs
    model_config = ConfigDict(
            json_schema_extra={
                "example": {
                    "subtotal": 100.00,
                    "tax_rate": .08,
                    "user_id": "user-1234567890"
                }
            }
        )


class CheckoutResponseModel(BaseModel):
    checkout_id: str
    status: str 
    subtotal: Decimal
    tax: Decimal
    total: Decimal 



class CheckoutStatusEnum(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
