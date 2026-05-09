# 🏠 Property Rental Management SaaS Platform

A full-stack multi-tenant SaaS platform for managing rental properties.

Owners can:
- Add and manage properties
- Approve or reject lease requests
- Track rent payments
- Manage maintenance requests

Tenants can:
- Browse properties
- Request leases
- Pay rent online
- Submit maintenance requests

---

## 🚀 Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- JWT Authentication
- Stripe Payments
- SQLite (default)

### Frontend
- React + Vite
- Axios
- React Router
- Tailwind CSS

---

# 📁 Project Structure

property-rental-saas/
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── database.py
│   │   ├── config.py
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env
│
├── .env.example
└── README.md

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd property-rental-saas


2️⃣ Backend Setup
cd backend
python -m venv venv
Windows
venv\Scripts\activate

Mac/Linux
source venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Copy Environment File
copy ..\.env.example .env

(Use cp ../.env.example .env on Mac/Linux)

Run Database Migrations
alembic upgrade head

Start Backend
uvicorn app.main:app --reload

Backend API:
http://localhost:8000

Swagger Docs:
http://localhost:8000/docs

3️⃣ Frontend Setup
cd ../frontend
npm install
npm run dev

Frontend:
http://localhost:5173

🔐 Authentication

JWT-based authentication with two roles:

owner
tenant

Endpoints:

POST /auth/register
POST /auth/login
🏘️ Property Workflow
Owner
Register as owner
Create property listings
Upload property images
View lease requests
Approve/reject leases
Track payments
Manage maintenance
Tenant
Register as tenant
Browse properties
Request lease
Wait for approval
Pay rent
Raise maintenance requests

📄 Lease Workflow Explanation
Step 1: Tenant Requests Lease

Tenant selects a property and submits:

Start date
End date
Monthly rent
Optional notes

Status = pending

Step 2: Owner Reviews Request

Owner can:

Approve
Reject
Step 3: Lease Activated

If approved:

Lease status → active
Property status → occupied
Step 4: Rent Payments

Tenant pays rent via Stripe.
Each payment is stored in database.

Step 5: Lease Completion

At end date:

Lease status → completed
Property status → available

💳 Payment Integration (Stripe)
Create Stripe Account

Sign up at https://stripe.com

Add Keys to .env
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
Backend Endpoints
Create Checkout Session

POST /payments/create-checkout-session

Stripe Webhook

POST /payments/webhook

List Payments

GET /payments

Payment Flow
Tenant clicks "Pay Rent"
Frontend calls checkout session API
Stripe checkout page opens
Tenant completes payment
Stripe webhook confirms payment
Payment saved in database
Lease payment status updated

🔧 Maintenance Workflow
Tenant creates maintenance request
Owner reviews request
Owner updates status:
open
in_progress
resolved
Tenant receives notification

📧 Notifications

Email notifications are sent for:

Lease approved
Lease rejected
Payment successful
Maintenance status updates

🗄️ Database Models
User
Property
PropertyImage
Lease
Payment
MaintenanceRequest

🏗️ Architecture Overview
Backend Layers
Routers

API endpoints.

Schemas

Pydantic validation.

Models

SQLAlchemy ORM models.

Services

Business logic.

Utils

Helpers like auth and email.

Database

Session management.

Request Flow

Frontend → API Router → Service Layer → Database → Response

📚 Main API Endpoints
Auth
POST /auth/register
POST /auth/login
Properties
GET /properties
POST /properties
GET /properties/{id}
PUT /properties/{id}
DELETE /properties/{id}
Leases
POST /leases/request
GET /leases
PUT /leases/{id}/approve
PUT /leases/{id}/reject
Payments
POST /payments/create-checkout-session
POST /payments/webhook
GET /payments
Maintenance
POST /maintenance
GET /maintenance
PUT /maintenance/{id}

🧪 Testing

Run backend tests:

pytest
🚀 Deployment
Backend
Render
Railway
AWS EC2
Frontend
Vercel
Netlify
Database
PostgreSQL

🔒 Security Features
Password hashing with bcrypt
JWT authentication
Role-based authorization
Stripe webhook verification
Input validation

📸 Screens
Login/Register
Owner Dashboard
Tenant Dashboard
Property Details
Lease Management
Payment History
Maintenance Requests