import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_product(name):
    """Creates a product in Stripe."""
    product = stripe.Product.create(name=name)
    return product['id']

def create_stripe_price(amount, product_id):
    """Creates a price in Stripe."""
    price = stripe.Price.create(
        unit_amount=int(amount * 100),
        currency="usd",
        product=product_id,
    )
    return price['id']

def create_stripe_session(price_id):
    """Creates a checkout session in Stripe."""
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session['id'], session['url']

def retrieve_stripe_session(session_id):
    """Retrieves a stripe session to check status."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session['payment_status']
