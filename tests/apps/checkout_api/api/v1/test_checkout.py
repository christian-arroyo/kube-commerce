from fastapi.testclient import TestClient

from apps.checkout_api.main import app
from apps.checkout_api.models.checkout_model import CheckoutStatusEnum

client = TestClient(app)

def get_sample_checkout_request() -> dict:
    return {
        "user_id": "12345",
        "subtotal": 29.98,
        "tax_rate": 0.099
    }

def test_create_checkout():
    response = client.post("/checkout", json=get_sample_checkout_request(), headers={"Idempotency-Key": "key-create"})
    assert response.status_code == 200
    response = client.post("/checkout", json={"incorrect": "data"})
    assert response.status_code == 422

def test_get_checkout():
    post_response = client.post("/checkout", json=get_sample_checkout_request(), headers={"Idempotency-Key": "key-get"})
    response = client.get(f"/checkout/{post_response.json()['checkout_id']}")
    assert response.status_code == 200
    response = client.get("/checkout/checkout-non-existent")
    assert response.status_code == 404

def test_complete_checkout():
    checkout_response = client.post("/checkout", json=get_sample_checkout_request(), headers={"Idempotency-Key": "key-complete"})
    complete_response = client.post(f"/checkout/{checkout_response.json()['checkout_id']}/complete")
    assert complete_response.status_code == 200
    assert complete_response.json()["status"] == CheckoutStatusEnum.COMPLETED.value

def test_cancel_checkout():
    checkout_response = client.post("/checkout", json=get_sample_checkout_request(), headers={"Idempotency-Key": "key-cancel"})
    cancel_response = client.post(f"/checkout/{checkout_response.json()['checkout_id']}/cancel")
    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == CheckoutStatusEnum.CANCELLED.value

def test_create_checkout_idempotency():
    headers = {"Idempotency-Key": "key-idempotency"}
    response1 = client.post("/checkout", json=get_sample_checkout_request(), headers=headers)
    response2 = client.post("/checkout", json=get_sample_checkout_request(), headers=headers)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["checkout_id"] == response2.json()["checkout_id"]
