## Running the Loan API Locally!

Follow these steps to run the application on your machine using Docker & Docker Compose.

### ✅ 1. Clone the Repository
git clone https://github.com/aditirajput18/dummy-branch-app

cd dummy-branch-app

### ✅ 2. Generate HTTPS Certificates (Local Only)

The application runs on https://branchloans.com
 locally.

mkdir certs

openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=branchloans.com"

### ✅ 3. Add Local Domain Mapping

Edit your /etc/hosts (Linux/macOS) or C:\Windows\System32\drivers\etc\hosts:


127.0.0.1 

branchloans.com

### ✅ 4. Run the Application

Choose your environment:

Development

ENV=dev docker compose up --build

Staging

ENV=staging docker compose up --build -d

Production

ENV=prod docker compose up --build -d

### 🌐 Local URLs
Purpose	URL

Health Check	https://branchloans.com/health

List Loans	https://branchloans.com/api/loans

Stats	https://branchloans.com/api/stats

### 🔄 Switching Between Environments

The environment is controlled by:

ENV=<env_name>


#### Valid values:

dev

staging

prod

#### Your compose file will automatically load:

env/.env.dev

env/.env.staging

env/.env.prod


#### This changes:

Logging level

Database name & credentials

Flask mode

Resource usage

Behavior & performance

Example:

ENV=prod docker compose up --build -d

## 🔧 Environment Variables (Explained)

Below is what each variable in your .env.* files means:

Variable	Description
ENV	Defines current environment (dev/staging/prod)
POSTGRES_DB	Database name used by PostgreSQL
POSTGRES_USER	Username for PostgreSQL
POSTGRES_PASSWORD	Password for the database
DATABASE_URL	Complete SQLAlchemy connection string
FLASK_ENV	Flask runtime mode (development/production)
LOG_LEVEL	Logging level (DEBUG / INFO / WARNING)

Example:

DATABASE_URL=postgresql://postgres:devpass@db:5432/loans_dev

## 🚀 CI/CD Pipeline (GitHub Actions)

Every push to main runs the full CI/CD pipeline:

### 1️⃣ Test Stage

Installs dependencies

Runs Python tests with pytest

If tests fail → pipeline stops

### 2️⃣ Build Stage

Builds Docker image using the repo source code

Tags image using the commit SHA

### 3️⃣ Security Scan (Trivy)

Scans Docker image for vulnerabilities

If CRITICAL issues are found → pipeline fails

### 4️⃣ Push Stage

Pushes Docker image to GitHub Container Registry (GHCR)

Only happens when pushing to the main branch

Pull Requests do NOT push images

## 🔐 Secrets Managed Securely

No secrets exist in code.

Sensitive credentials (if any) should be stored in:

GitHub → Settings → Secrets → Actions

## 🏗 Architecture Diagram (ASCII)
                ┌──────────────────────────┐
                │      GitHub Actions       │
                │  (CI/CD: Test → Build →  │
                │   Scan → Push Image)     │
                └─────────────┬────────────┘
                              │
                              ▼
                  Docker Image (GHCR)
                              │
               ┌──────────────┴──────────────┐
               │                               │
        ┌──────▼───────┐                 ┌────▼────────┐
        │   Loan API    │  HTTPS :443     │ PostgreSQL  │
        │ (Flask + Gunicorn)──────────────▶│   Database  │
        │     Docker     │                 └─────────────┘
        └───────────────┘
               ▲
               │
               │ Local Host Mapping
               │ 127.0.0.1 → branchloans.com
               │
        ┌──────┴────────┐
        │   Browser      │
        │ https://branchloans.com │
        └────────────────┘
