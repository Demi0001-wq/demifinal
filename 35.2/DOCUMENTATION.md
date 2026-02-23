# Project Documentation

This file explains how the LMS backend works and how to use its features.

## API Documentation

We use drf-spectacular to make documentation automatically. You can see it in your browser when the server is running:

- Swagger UI: http://127.0.0.1:8000/api/docs/swagger/
- Redoc: http://127.0.0.1:8000/api/docs/redoc/

If you need the raw schema for tools like Postman, you can get it at:
- Schema: http://127.0.0.1:8000/api/schema/

## Stripe Payments

I integrated Stripe to handle buying courses and lessons. Here is how it works:

1. Setup: You need a Stripe API key. Put it in config/settings.py as STRIPE_API_KEY.
2. Flow:
   - When a user wants to buy something, they call /api/users/payments/create/.
   - The server creates a Product and a Price in Stripe.
   - Then it creates a Checkout Session and gives you a link.
   - The user goes to that link to pay.
3. Checking status: You can call /api/users/payments/status/<id>/ to see if the payment was successful.

We use the official stripe-python library for this.

## Permissions and Roles

There are three main ways to access the API:

- Public: Anyone can register or log in.
- Owners: If you create a course or lesson, you are the owner and can edit or delete it.
- Moderators: People in the Moderator group can see all courses and lessons and edit them, but they cannot create new ones or delete them.

## Validators

I added a validator for video links. It only allows links that start with https://www.youtube.com/ or https://youtube.com/. This is to keep the content educational.

## Pagination

To keep the API fast, I limited the number of items per page to 10. You can use the ?page= query parameter to see more results.
