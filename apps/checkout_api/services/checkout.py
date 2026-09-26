""" This module contains the business logic for the CheckoutService class"""

from decimal import Decimal, ROUND_HALF_UP
import uuid
from fastapi import HTTPException
import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session
from apps.checkout_api.db.schema import Checkout, IdempotencyKey
from apps.checkout_api.models.checkout_model import CheckoutRequestModel, CheckoutResponseModel, CheckoutStatusEnum

class CheckoutService:
    def __init__(self, session: Session):
        self._db = session

    def _calculate_order_total(self, subtotal: Decimal, tax_rate: Decimal) -> Decimal:
        total = subtotal + (subtotal * tax_rate)
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _calculate_tax_total(self, subtotal: Decimal, tax_rate: Decimal) -> Decimal:
        tax = subtotal * tax_rate
        return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _change_checkout_status(self, checkout: Checkout, status: CheckoutStatusEnum) -> Checkout:
        checkout.status = status
        self._db.commit()
        self._db.refresh(checkout)
        return checkout

    def _generate_checkout_id(self) -> str:
        checkout_id = str(uuid.uuid4())
        id = "checkout-" + checkout_id
        return id

    def create_checkout(self, request: CheckoutRequestModel, idempotency_key: str) -> Checkout:
        body_hash = hashlib.sha256(json.dumps(request.model_dump(), sort_keys=True, default=str).encode()).hexdigest()

        existing = self._db.get(IdempotencyKey, idempotency_key)
        if existing:
            if existing.body_hash != body_hash:
                raise HTTPException(status_code=422, detail="Idempotency key reused with a different request body")
            return self.get_checkout(existing.checkout_id)
        checkout_id = self._generate_checkout_id()
        total = self._calculate_order_total(request.subtotal, request.tax_rate)
        tax = self._calculate_tax_total(request.subtotal, request.tax_rate)
        checkout = Checkout(
            checkout_id=checkout_id,
            status=CheckoutStatusEnum.PENDING,
            subtotal=request.subtotal,
            tax=tax,
            tax_rate=request.tax_rate,
            total=total,
            user_id=request.user_id)
        # Write to database
        self._db.add(checkout)
        self._db.add(IdempotencyKey(key=idempotency_key, body_hash=body_hash, checkout_id=checkout_id))
        self._db.commit()
        self._db.refresh(checkout)
        return checkout

    def cancel_checkout(self, checkout_id: str) -> Checkout:
        checkout = self.get_checkout(checkout_id)
        # Raise exception if trying to cancel a completed checkout
        if checkout.status == CheckoutStatusEnum.COMPLETED:
            raise HTTPException(status_code=409, detail=f"Checkout with ID {checkout_id} is completed, cannot cancel")
        return self._change_checkout_status(checkout, CheckoutStatusEnum.CANCELLED)
    
    def complete_checkout(self, checkout_id: str) -> Checkout:
        checkout = self.get_checkout(checkout_id)
        # Raise exception if trying to complete a cancelled checkout
        if checkout.status == CheckoutStatusEnum.CANCELLED:
            raise HTTPException(status_code=409, detail=f"Checkout with ID {checkout_id} is cancelled, cannot complete")
        return self._change_checkout_status(checkout, CheckoutStatusEnum.COMPLETED)

    def get_checkout(self, checkout_id: str) -> Checkout:
        stmt = select(Checkout).where(Checkout.checkout_id == checkout_id)
        response = self._db.execute(stmt).scalars().first()
        if not response:
            raise HTTPException(status_code=404, detail=f"Checkout with ID {checkout_id} not found")
        return response
