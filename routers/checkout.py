import os
import stripe
from fastapi import APIRouter, responses

router = APIRouter(
    prefix="/checkout",
    responses={404: {"description": "Not found"}}
)

stripe.api_key = os.getenv('STRIPE_API_KEY')

@router.post("/")
def create_payment():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': 'price_id',
                'quantity': 1,
            }],
            mode='payment',
            success_url=os.getenv('BASE_URL') + '/success',
            cancel_url=os.getenv('BASE_URL') + '/cancel',
        )
        return checkout_session.id
    except Exception as e:
        return str(e)
