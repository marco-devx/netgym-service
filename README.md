# NetGym Service

> **⚾ Baseball Player Management & AI Bio Generation**

**NetGym Service** is a comprehensive backend API built with **FastAPI**, following **Clean Architecture** principles and **Domain-Driven Design (DDD)**. It manages baseball players, gym activities, and leverages **Generative AI** to create dynamic player biographies.

The system uses **PostgreSQL** as its database engine and supports **Multi-tenancy**.

---

## 🚀 Key Features

*   **RESTful API**: Built with FastAPI for high performance.
*   **AI Integration**: **OpenAI** integration for generating creative player biographies.
*   **Clean Architecture**: Separation of concerns into Domain, Application, and Infrastructure layers.
*   **Multi-tenancy**: Robust support for multiple tenants with isolated data.
*   **Database**: Native support for **PostgreSQL** with **SQLAlchemy** & **SQLModel**.
*   **Authentication**: JWT-based authentication with role management.
*   **Validation**: Robust data validation using Pydantic v2.
*   **Containerization**: Docker and Docker Compose support for easy deployment.
*   **Testing**: Comprehensive test suite with pytest.

---

## 🛠️ Technology Stack

*   **Language**: Python 3.13
*   **Framework**: FastAPI
*   **AI/LLM**: OpenAI API
*   **ORM**: SQLAlchemy & SQLModel
*   **Migrations**: Alembic
*   **Dependency Management**: Pipenv
*   **Database**: PostgreSQL
*   **Testing**: Pytest, Pytest-cov
*   **Code Quality**: Black, Isort, Flake8, Pylint

---

## 🏗️ Project Structure

The project follows a strict **Hexagonal Architecture** (Ports & Adapters) structure within the `src/` directory:

```text
src/
├── application/                # Application Layer (Use Cases, DTOs)
│   ├── dtos/                   # Data Transfer Objects
│   ├── services/               # Application Services
│   └── use_cases/              # Business Logic Execution
│
├── domain/                     # Domain Layer (Enterprise Logic)
│   ├── entities/               # Domain Entities
│   ├── factories/              # Object Creation Strategies
│   ├── ports/                  # Interfaces (Repositories, Services)
│   │   ├── repositories/       # Repository Interfaces
│   │   └── services/           # Service Interfaces
│   ├── domain_services/        # Domain-specific logic
│   └── value_objects/          # Immutable Domain Objects
│
├── infrastructure/             # Infrastructure Layer (External Details)
│   ├── config/                 # Settings & Database Config
│   ├── controllers/            # API Routes (FastAPI)
│   ├── models/                 # ORM Models (SQLAlchemy)
│   ├── repositories/           # Data Access Implementations
│   └── migrations/             # Alembic Scripts
│
└── shared/                     # Shared Utilities & Constants
    ├── exceptions/             # Custom Exceptions
    └── utils/                  # Helper Functions
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites

*   Python 3.13+
*   Pipenv (`pip install --user pipenv`)
*   Docker & Docker Compose (optional, for database)
*   PostgreSQL (if not using Docker)

### 2. Clone and Install

```bash
git clone [REPOSITORY_URL]
cd netgym-service

# Install dependencies
pipenv install --dev
pipenv shell
```

### 3. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

> **Note**: Update database credentials (`DB_USER`, `DB_PASS`, etc.) and **OpenAI API Key** (`OPENAI_API_KEY`) in `.env`.

---

## 🐳 Docker Setup (Database)

We provide a Docker Compose file to easily spin up a database instance.

```bash
docker-compose -f docker-compose.yml up -d
```

*This command starts a container with PostgreSQL.*

---

## 📦 Database Migrations (Alembic)

We use Alembic to manage database schema updates, supporting multi-tenancy.

### 1. Create a New Migration

Generates a new migration file based on model changes.

```bash
pipenv run makemigration "description_of_change"

# OR manually:
alembic -c src/infrastructure/config/migrations/alembic.ini revision --autogenerate -m "description_of_change"
```

### 2. Apply Migrations (Upgrade)

Updates the database to the latest version.

```bash
alembic -c src/infrastructure/config/migrations/alembic.ini upgrade head
```

### 3. Revert Migrations (Downgrade)

Reverts the last migration.

```bash
alembic -c src/infrastructure/config/migrations/alembic.ini downgrade -1
```

### 4. Multi-Tenant Migrations

To manage migrations across all tenants:

```bash
# Apply to all tenants
pipenv run migrate-all

# Downgrade all tenants
pipenv run downgrade-all
```

---

## ▶️ Running the Application

### Development Mode

Start the server with hot reload:

```bash
pipenv run start

# OR manually:
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
-   **API**: http://localhost:8000
-   **Swagger Docs**: http://localhost:8000/docs
-   **ReDoc**: http://localhost:8000/redoc

### Docker

To run the full application stack via Docker:

```bash
docker-compose up --build -d
```

---

## 🧪 Testing & Code Quality

Run the test suite and quality checks using the scripts defined in `Pipfile`:

### Run Tests

```bash
# Run all tests
pipenv run test

# Run with coverage report
pipenv run coverage
```

### Code Quality

```bash
# Format code (Black & Isort)
pipenv run format

# Run linters (Flake8 & Pylint)
pipenv run lint
```

---

## 🔒 Security

```bash
# Run security checks
pipenv run bandit -r src/

# Check for vulnerable dependencies
pipenv run safety check
```

---

## 🤝 Contributing

1.  Create a feature branch (`git checkout -b feature/amazing-feature`)
2.  Make your changes following the architecture patterns
3.  Write tests for your changes
4.  Run quality checks (`pipenv run format && pipenv run lint && pipenv run test`)
5.  Commit your changes (`git commit -m 'Add amazing feature'`)
6.  Push to the branch (`git push origin feature/amazing-feature`)
7.  Open a Pull Request

---

## 👥 Authors

*   **NetGym Team**
