""" This module contains the business logic for the CheckoutService class"""

from decimal import Decimal, ROUND_HALF_UP
import uuid
from fastapi import HTTPException

from apps.checkout_api.db.db import get_database
from apps.checkout_api.models.checkout import CheckoutRequestModel, CheckoutResponseModel, CheckoutStatusEnum

class CheckoutService:
    def __init__(self):
        pass

    def _calculate_order_total(self, subtotal, tax_rate) -> Decimal:
        total = subtotal + (subtotal * tax_rate)
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _calculate_tax_total(self, subtotal, tax_rate) -> Decimal:
        tax = subtotal * tax_rate
        return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _change_checkout_status(self, checkout_id: str, status: CheckoutStatusEnum) -> CheckoutResponseModel:
        checkout = self.get_checkout(checkout_id)
        checkout.status = status
        return checkout

    def _generate_checkout_id(self) -> str:
        checkout_id = str(uuid.uuid4())
        id = "checkout-" + checkout_id
        return id

    def create_checkout(self, request: CheckoutRequestModel) -> CheckoutResponseModel:
        checkout_id = self._generate_checkout_id()
        total = self._calculate_order_total(request.subtotal, request.tax_rate)
        tax = self._calculate_tax_total(request.subtotal, request.tax_rate)
        # Save data in repository
        # Change this after implementing database storage for checkout data
        checkout_response = CheckoutResponseModel(checkout_id=checkout_id, status=CheckoutStatusEnum.PENDING, subtotal=request.subtotal, tax=tax, total=total)
        get_database()[checkout_id] = checkout_response
        return checkout_response
        # Call Go Payment service
        # Store checkout result
        # Return completed or failed status

    def cancel_checkout(self, checkout_id: str) -> CheckoutResponseModel:
        return self._change_checkout_status(checkout_id, CheckoutStatusEnum.CANCELLED)
    
    def complete_checkout(self, checkout_id: str) -> CheckoutResponseModel:
        return self._change_checkout_status(checkout_id, CheckoutStatusEnum.COMPLETED)

    def get_checkout(self, checkout_id: str) -> CheckoutResponseModel:
        database = get_database()
        if checkout_id in database:
            return database[checkout_id]
        raise HTTPException(status_code=404, detail=f"Checkout {checkout_id} not found")
