from fastapi.testclient import TestClient

from apps.checkout_api.main import app

client = TestClient(app)

def get_sample_checkout_request() -> dict:
    return {
        "user_id": "12345",
        "items": [
            {"item_number": 12345, "price": 19.99, "description": "Black Nike Shoes"},
            {"item_number": 45678, "price": 9.99, "description": "Black Nike Shorts"}
        ],
        "subtotal": 29.98,
        "tax_rate": 0.099
    }

def test_create_checkout():
    response = client.post("/checkout", json=get_sample_checkout_request())
    assert response.status_code == 200
    response = client.post("/checkout", json={"incorrect": "data"})
    assert response.status_code == 422

def test_get_checkout():
    post_response = client.post("/checkout", json=get_sample_checkout_request())
    response = client.get(f"/checkout/{post_response.json()['checkout_id']}")
    assert response.status_code == 200
    response = client.get("/checkout/checkout-non-existent")
    assert response.status_code == 404


def test_complete_checkout():
    response = client.post("/checkout/checkout-0/complete")
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"

def test_cancel_checkout():
    response = client.post("/checkout/checkout-0/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"
