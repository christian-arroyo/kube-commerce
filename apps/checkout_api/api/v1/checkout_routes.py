"""This module contains the routes for the checkout API"""

from fastapi import APIRouter, Body

from apps.checkout_api.models.checkout import CheckoutRequestModel, CheckoutResponseModel
from apps.checkout_api.services.checkout import CheckoutService

router = APIRouter()

def get_checkout_service() -> CheckoutService:
    return CheckoutService()

# POST /api/v1/checkouts -- Create a checkout in PENDING status
@router.post("/checkout")
async def create_checkout(body: CheckoutRequestModel = Body(...)) -> CheckoutResponseModel:
    checkout_service = get_checkout_service()
    return checkout_service.create_checkout(body)

# Get checkout object by ID
@router.get("/checkout/{checkout_id}")
def get_checkout(checkout_id: str):
    checkout_service = get_checkout_service()
    return checkout_service.get_checkout(checkout_id)

@router.post("/checkout/{checkout_id}/complete")
def complete_checkout(checkout_id: str):
    checkout_service = get_checkout_service()
    return checkout_service.complete_checkout(checkout_id)

@router.post("/checkout/{checkout_id}/cancel")
def cancel_checkout(checkout_id: str):
    checkout_service = get_checkout_service()
    return checkout_service.cancel_checkout(checkout_id)

