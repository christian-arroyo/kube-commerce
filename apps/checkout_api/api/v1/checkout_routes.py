"""This module contains the routes for the checkout API"""

from fastapi import APIRouter, Body, Depends, Header

from apps.checkout_api.db.schema import SessionLocal
from apps.checkout_api.models.checkout_model import CheckoutRequestModel, CheckoutResponseModel
from apps.checkout_api.services.checkout import CheckoutService

router = APIRouter()

def get_checkout_service() -> CheckoutService:
    return CheckoutService(session=SessionLocal())

# POST /api/v1/checkouts -- Create a checkout in PENDING status
@router.post("/checkout", response_model=CheckoutResponseModel)
async def create_checkout(checkout: CheckoutRequestModel, idempotency_key: str = Header(..., alias="Idempotency-Key"), 
                          service: CheckoutService = Depends(get_checkout_service)):
    return service.create_checkout(checkout, idempotency_key)

# Get checkout object by ID
@router.get("/checkout/{checkout_id}", response_model=CheckoutResponseModel)
def get_checkout(checkout_id: str, service: CheckoutService = Depends(get_checkout_service)):
    return service.get_checkout(checkout_id)

@router.post("/checkout/{checkout_id}/complete", response_model=CheckoutResponseModel)
def complete_checkout(checkout_id: str, service: CheckoutService = Depends(get_checkout_service)):
    return service.complete_checkout(checkout_id)

@router.post("/checkout/{checkout_id}/cancel", response_model=CheckoutResponseModel)
def cancel_checkout(checkout_id: str, service: CheckoutService = Depends(get_checkout_service)):
    return service.cancel_checkout(checkout_id)
