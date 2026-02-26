import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    return stripe.Product.create(name=name)['id']


def create_stripe_price(amount, product_id):
    return stripe.Price.create(
        unit_amount=int(amount * 100),
        currency="usd",
        product=product_id
    )['id']


def create_stripe_session(price_id):
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment"
    )
    return session['id'], session['url']


def retrieve_stripe_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)['payment_status']
