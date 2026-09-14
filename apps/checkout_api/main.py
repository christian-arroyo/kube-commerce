
"""
The checkout API creates a checkout call to the payment service
Calculates subtotal, tax, and total for the order
Creates a checkout with payment_pending status and returns the checkout id to the client
Calls the payment service to process the payment and updates the checkout status to paid or failed
"""
from fastapi import FastAPI
from apps.checkout_api.core.logging import setup_logging
from apps.checkout_api.api.v1 import checkout_routes

setup_logging()

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to my checkout API!"}

# Register routes
app.include_router(checkout_routes.router)
