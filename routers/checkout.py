import json
import os
import stripe
from fastapi import APIRouter, responses

router = APIRouter(
    prefix="/checkout",
    responses={404: {"description": "Not found"}}
)

stripe.api_key = os.getenv('STRIPE_API_KEY')

@router.get("/")
def create_checkout_session(price: int):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "FastAPI Stripe Checkout",
                        },
                        "unit_amount": price * 100,
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "user_id": 3,
                "email": "abc@gmail.com",
                "request_id": 1234567890
            },
            mode="payment",
            success_url=os.getenv("BASE_URL") + "/success/",
            cancel_url=os.getenv("BASE_URL") + "/cancel/",
            customer_email="ping@fastapitutorial.com",
        )
        return responses.RedirectResponse(checkout_session.url, status_code=303)

    except stripe.error.CardError as e:
        # Handle specific Stripe errors
        return {"status": "error", "message": str(e)}
    except stripe.error.StripeError as e:
        # Handle generic Stripe errors
        return {"status": "error", "message": "Something went wrong. Please try again later."}