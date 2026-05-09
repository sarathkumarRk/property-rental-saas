import stripe
from app.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount: int):

    intent = stripe.PaymentIntent.create(
        amount=amount * 100,
        currency="usd"
    )

    return intent