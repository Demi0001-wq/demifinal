# LMS Project

This is a backend project for a Learning Management System made with Django and Django REST Framework.

## Features

This project includes user management where you can log in with your email. I used SimpleJWT for authentication. There are different roles like Moderators and Owners to handle who can see or edit the courses.

The materials app has Courses and Lessons. I added a way for users to subscribe to courses. I also made a validator to make sure video links are only from youtube.com.

For payments, I integrated Stripe. It can create products and prices, and then give a checkout link. You can also check the status of a payment.

Documentation is handled by drf-spectacular. You can see the Swagger or Redoc pages to check the endpoints.

## Tech Stack
- Django and DRF
- SimpleJWT for auth
- Stripe for payments
- drf-spectacular for docs
- SQLite

## How to setup (Local)

1. Install everything from requirements.txt:
   pip install -r requirements.txt

2. Put your Stripe key in config/settings.py:
   STRIPE_API_KEY = 'your_key_here'

3. Run the migrations:
   python manage.py migrate

# LMS Project

This is a backend project for a Learning Management System made with Django and Django REST Framework.

## Features

This project includes user management where you can log in with your email. I used SimpleJWT for authentication. There are different roles like Moderators and Owners to handle who can see or edit the courses.

The materials app has Courses and Lessons. I added a way for users to subscribe to courses. I also made a validator to make sure video links are only from youtube.com.

For payments, I integrated Stripe. It can create products and prices, and then give a checkout link. You can also check the status of a payment.

Documentation is handled by drf-spectacular. You can see the Swagger or Redoc pages to check the endpoints.

## Tech Stack
- Django and DRF
- SimpleJWT for auth
- Stripe for payments
- drf-spectacular for docs
- SQLite

## How to setup (Local)

1. Install everything from requirements.txt:
   pip install -r requirements.txt

2. Put your Stripe key in config/settings.py:
   STRIPE_API_KEY = 'your_key_here'

3. Run the migrations:
   python manage.py migrate

4. You can fill some test payment data:
   python manage.py fill_payments

5. Start the server:
   python manage.py runserver

## How to setup (Docker)

1. **Create .env file**: 
   Copy `env.sample` to `.env` and fill in your variables (like `STRIPE_API_KEY`).
   ```bash
   cp env.sample .env
   ```

2. **Build and start the containers**:
   ```bash
   docker-compose up --build -d
   ```

## Remote Server Setup (CI/CD)

To fulfill the project requirements for remote deployment:

### 1. Server Configuration (Ubuntu)
- Install Docker and Docker Compose.
- Install Nginx and configure it as a reverse proxy for the backend.
- Ensure ports 80 (HTTP) and 22 (SSH) are open.
- Use SSH keys for secure access (place your public key in `~/.ssh/authorized_keys`).

### 2. GitHub Secrets
Configure the following secrets in your GitHub repository (`Settings -> Secrets and variables -> Actions`):
- `SERVER_HOST`: Your server's IP address or domain.
- `SERVER_USER`: Your SSH username (e.g., `ubuntu`).
- `SERVER_SSH_KEY`: Your private SSH key (RSA/ED25519).
- `DJANGO_SECRET_KEY`: A secure random string for Django's `SECRET_KEY`.
- `STRIPE_API_KEY`: Your Stripe secret api key (Example: `sk_test_...`).

### 3. CI/CD Workflow
The project includes a GitHub Actions workflow in `.github/workflows/deploy.yml` that:
1. Runs tests on every push to `develop` or `main`.
2. Automatically deploys to the remote server if tests pass.

## Endpoints

- Login: /api/users/login/
- Token Refresh: /api/users/token/refresh/
- Courses: /api/materials/courses/
- Lessons: /api/materials/lessons/
- Subscribe: /api/materials/course/subscribe/
- Create Payment: /api/users/payments/create/
- Payment Status: /api/users/payments/status/id/

## Testing
You can run tests with:
```bash
python manage.py test
```
Or inside Docker:
```bash
docker-compose exec backend python manage.py test
```

I also used coverage to check how much of the code is tested.


## CI/CD and Automation

This project uses GitHub Actions for continuous integration and deployment.

### GitHub Actions Workflow

The workflow is defined in \.github/workflows/deploy.yml\ and performs:
1.  **Testing**: Automatically runs Django tests on every push and pull request.
2.  **Deployment**: Automatically deploys the code to the remote server if tests pass.

### Remote Server Setup

To enable automated deployment, your remote server should:
1.  Have **Docker** and **Docker Compose** installed.
2.  Have the project repository cloned at \~/app/docker\.
3.  Configure **SSH key access** and add the private key to GitHub Secrets.

### GitHub Secrets Configuration

For the workflow to work, add the following secrets in your GitHub repository settings (Settings > Secrets and variables > Actions**):

- \DJANGO_SECRET_KEY\: Your Django secret key.
- \SERVER_HOST\: IP address or domain of your remote server.
- \SERVER_USER\: SSH username (e.g., \
oot\ or \ubuntu\).
- \SERVER_SSH_KEY\: Your private SSH key.
- \SERVER_SSH_PASSPHRASE\: (Optional) Passphrase for your SSH key.

For other variables (Stripe, Email), refer to \env.sample\ and add them as secrets if you wish to inject them during deployment.

---




