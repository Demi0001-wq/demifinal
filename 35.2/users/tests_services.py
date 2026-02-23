from django.test import TestCase
from unittest.mock import patch
from users.services import create_stripe_product, create_stripe_price, create_stripe_session, retrieve_stripe_session

class StripeServiceTestCase(TestCase):
    @patch('stripe.Product.create')
    def test_create_stripe_product(self, mock_create):
        mock_create.return_value = {'id': 'prod_123'}
        product_id = create_stripe_product('Test Product')
        self.assertEqual(product_id, 'prod_123')
        mock_create.assert_called_once_with(name='Test Product')

    @patch('stripe.Price.create')
    def test_create_stripe_price(self, mock_create):
        mock_create.return_value = {'id': 'price_123'}
        price_id = create_stripe_price(100.00, 'prod_123')
        self.assertEqual(price_id, 'price_123')
        mock_create.assert_called_once_with(
            unit_amount=10000,
            currency="usd",
            product='prod_123',
        )

    @patch('stripe.checkout.Session.create')
    def test_create_stripe_session(self, mock_create):
        mock_create.return_value = {'id': 'sess_123', 'url': 'https://stripe.com/pay'}
        session_id, payment_link = create_stripe_session('price_123')
        self.assertEqual(session_id, 'sess_123')
        self.assertEqual(payment_link, 'https://stripe.com/pay')

    @patch('stripe.checkout.Session.retrieve')
    def test_retrieve_stripe_session(self, mock_retrieve):
        mock_retrieve.return_value = {'payment_status': 'paid'}
        status = retrieve_stripe_session('sess_123')
        self.assertEqual(status, 'paid')
