# LMS Project (Django REST Framework)

This project is a Learning Management System (LMS) built with Django REST Framework, containerized with Docker, and automated with GitHub Actions.

## Features
- Django REST Framework: Core API.
- PostgreSQL: Primary database.
- Redis & Celery: Background task processing (e.g., deactivating inactive users).
- Nginx: Reverse proxy for serving static and media files.
- GitHub Actions: Automated testing, linting, and deployment.

## Local Setup

### Prerequisites
- Docker and Docker Compose installed.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Demi0001-wq/docker.git
   cd docker
   ```

2. Configure environment variables:
   - Copy `env.sample` to `.env`.
   - Update the values in `.env` (especially `SECRET_KEY` and `STRIPE_API_KEY`).

3. Run the project:
   ```bash
   docker compose up -d --build
   ```
   The application will be available at `http://localhost`.

4. Run tests:
   ```bash
   docker compose exec backend pytest
   ```

## Deployment

### Server Setup
1. Prepare the server:
   - Install Docker and Docker Compose.
   - Set up SSH access for GitHub Actions.

2. GitHub Secrets:
   - Add the following secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):
     - `SSH_HOST`: Your server's IP address.
     - `SSH_USER`: SSH username (e.g., `root` or `ubuntu`).
     - `SSH_KEY`: Your SSH private key.

3. Automatic Deployment:
   - Every push to the `main` branch will trigger the CI/CD pipeline:
     - Lint: Checks code style with `flake8`.
     - Test: Runs `pytest`.
     - Build: Verifies Docker images can be built.
     - Deploy: Automatically pulls changes and restarts containers on the server.

## Server Address
- Live App: [http://your-server-ip](http://your-server-ip) (Please replace with your actual server IP once deployed).
