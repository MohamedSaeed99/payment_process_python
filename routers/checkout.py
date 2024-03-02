import json
import os
import stripe
from fastapi import APIRouter, HTTPException, Request, responses

router = APIRouter(
    prefix="/process",
    responses={404: {"description": "Not found"}}
)

endpoint_secret = 'whsec_5c7db391c29bbfdff9a8ae08b0515dbdd9a1d24a3ba1aff54e65c2c26a0a49e3'
stripe.api_key = os.getenv('STRIPE_API_KEY')

@router.get("/checkout")
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
    

@router.post("/webhook/")
async def stripe_webhook(request: Request):
    payload = await request.body()
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    print(event)
    if event["type"] == "checkout.session.completed":
        payment = event["data"]["object"]
        amount = payment["amount_total"]
        currency = payment["currency"]
        user_id = payment["metadata"]["user_id"]
        user_email = payment["customer_details"]["email"]
        user_name = payment["customer_details"]["name"]
        order_id = payment["id"]
        # save to db
        # send email in background task
    return {}