<div align="center">
 <img width="524" src="lumitech_python_template_logo.png" />
</div>

# [Lumitech](https://lumitech.co/) Python FastAPI Template

Welcome to the Lumitech Python FastAPI Template. This template offers a solid foundation for building back-end applications with Python and FastAPI, featuring SQLAlchemy ORM, Redis, OpenAPI documentation, and a ready-to-use Docker setup. Designed with best practices in mind, it ensures maintainability, scalability, and reliability, making development efficient and production-ready.

### About Lumitech

[Lumitech](https://lumitech.co/) is a custom software development company providing professional services worldwide. We partner with technology businesses globally helping them to build successful engineering teams and create innovative software products. We're a global team of software engineers, AI and ML specialists, product managers, and technology experts who have achieved a 600% growth rate since 2022. When a rocket launches toward the moon, it doesn't stop halfway. Neither do we.

## 🛠️ Technology Stack:

- [Python](https://www.python.org/) - programming language;
- [FastAPI](https://fastapi.tiangolo.com/) - web framework;
- [Pydantic](https://docs.pydantic.dev/) - data validation and serialization;
- [OpenAPI](https://swagger.io/) - API documentation;
- [PostgreSQL](https://www.postgresql.org/) - relational database;
- [SQLAlchemy](https://www.sqlalchemy.org/) - database ORM;
- [Alembic](https://alembic.sqlalchemy.org/) - database migration tool;
- [Redis](https://redis.io/) - caching;
- [Docker](https://www.docker.com/) - containerization;
- [UV](https://docs.astral.sh/uv/) - package and project manager;
- [Pre-commit](https://pre-commit.com/) - managing and maintaining pre-commit hooks.

## 🔧 Environment Variables

Environment variables are listed in [_.env.example_](.env.example) file.

## 📌 Quick Start

- Navigate to the project directory via `cd <project_name>`;
- Copy [_.env.example_](.env.example) to _.env_ file via `cp .env.example .env`;
- Fill environment variables listed in _.env_ with relevant values;
- Create docker network via `docker network create <network_name>`;
- Run the project via `docker compose -f prod.docker-compose.yml up`.

  _NOTE: use `-d` flag to run containers in the background._

### 🔄 Running Database Migrations

The project uses Alembic for database migrations. Migrations are automatically applied when the container starts, as configured in the [_entrypoint.sh_](app/entrypoint.sh) file.

To create a new migration manually:

1. Make changes to your SQLAlchemy models;
2. Run `docker compose exec --user root fastapi alembic revision --autogenerate -m "<message>"`;
3. Review the generated migration file in app/database/migrations/versions/;
4. Apply the migration with `docker compose exec --user root fastapi alembic upgrade head`.

_NOTE: to downgrade the migration run `docker compose exec --user root fastapi alembic downgrade -1`._

## ⚙ Key Features

### 🧩 Repository Pattern

This template implements the Repository pattern to abstract database operations. The `BaseRepository` class provides a set of common CRUD operations that can be extended for specific entities.

#### Repository Usage Example:

```python
# Create a repository for a specific model.
class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    pass


user_repository = UserRepository(User)

# Fetch a user by ID.
user = await user_repository.fetch_one(id=user_id, session=session)

# Create a new user.
new_user = await user_repository.create(user_data, session)
```

### 🧠 Manager Pattern

The template uses a Manager pattern to implement business logic. The `BaseManager` class works with repositories and adds error handling and validation.

#### Manager Usage Example:

```python
# Create a manager for a specific model.
class UserManager(BaseManager[User, UserRepository, UserCreate, UserUpdate]):
    pass


user_manager = UserManager(User, UserRepository)

# Fetch a user by ID (with error handling).
try:
    user = await user_manager.fetch_one(id=user_id, session=session)
except HTTPNotFoundException:
    # Handle not found case.

# Create a new user.
new_user = await user_manager.create(user_data, session)
```

### 🐳 Docker

This template provides Docker configuration for both development and production environments:

1. **Development** - Uses [_dev.docker-compose.yml_](dev.docker-compose.yml) and [_dev.Dockerfile_](dev.Dockerfile) with hot-reloading for faster development.
2. **Production** - Uses [_prod.docker-compose.yml_](prod.docker-compose.yml) and [_prod.Dockerfile_](prod.Dockerfile) optimized for production use.

The Docker setup includes:

- FastAPI application;
- PostgreSQL database;
- Redis for caching;
- Traefik application proxy.

### 📖 API Documentation

The template includes OpenAPI documentation. When running the application, you can access the API documentation at:

- Swagger UI: `/docs`;
- ReDoc: `/redoc`.

## 📁 Project Structure

The project is organized into several modules to promote a clean architecture and separation of concerns:

```
.
├── README.md                        # Project overview and documentation
├── app                              # Main application package
│   ├── __init__.py
│   ├── alembic.ini                  # Alembic config file for migrations
│   ├── database                     # 🗃️ Database module
│   │   ├── __init__.py
│   │   ├── engine.py                # Sets up SQLAlchemy engine and session
│   │   ├── migrations               # Alembic migration directory
│   │   │   ├── env.py               # Alembic environment config
│   │   │   ├── script.py.mako       # Template for Alembic scripts
│   │   │   └── versions
│   │   │       └── 2025_04_06_...   # Example migration script
│   │   └── models.py                # SQLAlchemy ORM models
│   ├── entrypoint.sh                # Entrypoint for Docker container
│   ├── exceptions                   # 🚨 Custom exception handling
│   │   ├── __init__.py
│   │   ├── database.py              # DB-related exception classes
│   │   ├── handlers.py              # FastAPI exception handlers
│   │   └── http.py                  # Custom HTTP exceptions
│   ├── main.py                      # FastAPI app instance and startup logic
│   ├── manager                      # 🧠📊 Business logic layer (Manager Pattern)
│   │   ├── __init__.py
│   │   ├── base.py                  # Base manager with common logic
│   │   └── user.py                  # Business logic for user entity
│   ├── repository                   # 📦 Data access layer (Repository Pattern)
│   │   ├── __init__.py
│   │   ├── base.py                  # Generic CRUD operations
│   │   └── user.py                  # User-specific queries
│   ├── routes                       # 🌐 API endpoints
│   │   ├── __init__.py
│   │   ├── dependencies.py          # FastAPI dependencies (e.g., DB session)
│   │   ├── misc.py                  # Miscellaneous endpoints
│   │   └── user.py                  # User-related API routes
│   ├── schemas                      # 📐 Pydantic models for I/O
│   │   ├── __init__.py
│   │   └── user.py                  # User request/response schemas
│   ├── settings.py                  # App and environment configuration
│   └── utils                        # 🛠️ Utility functions and helpers
│       ├── __init__.py
│       ├── cache.py                 # Redis cache tools
│       ├── constants.py             # App-wide constants
│       ├── misc.py                  # General-purpose helpers
│       ├── mixins.py                # Mixin classes
│       ├── pagination.py            # Pagination helpers
│       ├── secrets.py               # Secret management
│       ├── tokens.py                # JWT creation/validation
│       └── types.py                 # Shared type definitions
├── dev.Dockerfile                   # Dockerfile for development
├── dev.docker-compose.yml          # Docker Compose config for dev
├── prod.Dockerfile                 # Dockerfile for production
├── prod.docker-compose.yml        # Docker Compose config for prod
├── pyproject.toml                  # Poetry project configuration
└── uv.lock                         # Poetry lockfile
```

## 👥 Contribution Guidelines

### 🛠️ Development Environment

- Install uv if needed via `curl -LsSf https://astral.sh/uv/install.sh | sh`;
- Navigate to the project directory via `cd <project_name>`;
- Create a virtual environment via `uv venv`;
- Activate the virtual environment via `source .venv/bin/activate`;
- Install the project's dependencies via `uv sync`;
- Initialize pre-commit environment and install pre-commit hooks via `pre-commit install`;
- Copy [_.env.example_](.env.example) to _.env_ file via `cp .env.example .env`;
- Fill environment variables listed in _.env_ with relevant values;
- Run the project via `docker compose -f dev.docker-compose.yml up`.

  _NOTE: use `-d` flag to run containers in the background._

### 📝 Conventional Commits

Follow commit message [conventions](https://www.conventionalcommits.org/en/v1.0.0/) to maintain a clean and consistent commit history:

- `feat`: a new feature.
- `fix`: a bug fix.
- `chore`: a routine task, maintenance.
- `refactor`: a refactoring or for a code change that neither fixes a bug nor adds a feature.
- `perf`: a code change that improves performance.
- `test`: for adding or modifying tests.
- `build`: for changes that affect the build system or external dependencies.
- `ci`: for changes related to CI/CD and scripts.
- `docs`: for documentation changes.
- `style`: for code style changes.

Each commit message should have the following format:

```
<type>(<?scope>): <description>

[optional body]

[optional footer]
```
