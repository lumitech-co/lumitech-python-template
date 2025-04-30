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

## 📌 Getting Started

### 🚀 Project Launch

#### 🌍 Production Environment

1. Navigate to the project directory via `cd <project_name>`;
2. Copy [_.env.example_](.env.example) to _.env_ file via `cp .env.example .env`;
3. Fill environment variables listed in _.env_ with relevant values;
4. Create docker network via `docker network create <network_name>`;
5. Run the project via `docker compose -f prod.docker-compose.yml up`.

_NOTE: use `-d` flag to run containers in the background._

#### 💻 Development Environment

1. Install uv if needed via `curl -LsSf https://astral.sh/uv/install.sh | sh`;
2. Navigate to the project directory via `cd <project_name>`;
3. Create a virtual environment via `uv venv`;
4. Activate the virtual environment via `source .venv/bin/activate`;
5. Install the project's dependencies via `uv sync`;
6. Initialize pre-commit environment and install pre-commit hooks via `pre-commit install`;
7. Copy [_.env.example_](.env.example) to _.env_ file via `cp .env.example .env`;
8. Fill environment variables listed in _.env_ with relevant values;
9. Run the project via `docker compose -f dev.docker-compose.yml up`.

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

This template implements the Repository pattern to abstract database operations. The `BaseRepository` class provides a set of common CRUD operations that can be extended for specific entities. Using a repository layer centralizes all database interactions, eliminates code duplication, and simplifies the integration of new entities. It enforces a clear contract for data access, isolates persistence logic from the rest of the application, and facilitates unit testing by enabling database operations to be easily mocked.

#### ✨ Repository Usage Example:

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

The template uses a Manager pattern to implement business logic. The `BaseManager` class works with repositories and adds error handling and validation. The manager layer separates business logic from database access and the presentation layer, resulting in a modular and maintainable architecture. It allows business rules to evolve independently of storage concerns, promotes reuse of logic across different operations, and improves overall scalability by clearly defining application service boundaries.

#### ✨ Manager Usage Example:

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

### 📜 Commits Format

Follows commit message [conventions](https://www.conventionalcommits.org/en/v1.0.0/) to maintain a clean and consistent commit history:

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

Each commit message has the following format:

```
<type>(<?scope>): <description>

[optional body]

[optional footer]
```

## 📁 Project Structure

The project is organized into several parts to promote a modular design, clean architecture, and separation of concerns:

`app/database`:

This directory handles data persistence and interaction with the database.

- `engine.py`: sets up the SQLAlchemy engine and session for database operations;
- `models.py`: defines the SQLAlchemy ORM models that represent database tables;
- `migrations/`: houses Alembic configuration and migration scripts to manage database schema changes.

`app/manager`:

Encapsulates the business logic layer using the Manager Pattern.

- `base.py`: provides a base manager with common logic used across different managers;
- `user.py`: contains user-specific business logic, orchestrating operations across repositories and utilities.

`app/repository`:

Implements the data access layer following the Repository Pattern.

- `base.py`: defines generic CRUD operations to be extended by specific repositories;
- `user.py`: implements user-specific data queries and operations.

`app/routes`:

Defines the API endpoints for the application using FastAPI.

- `user.py`: routes related to user management;
- `misc.py`: routes for miscellaneous endpoints;
- `dependencies.py`: Defines reusable FastAPI dependencies (e.g., database session injection).

`app/schemas`:

Manages input and output validation using Pydantic models.

- `user.py`: defines request and response schemas for user-related endpoints.

`app/exceptions`:

Centralizes error handling and custom exceptions.

- `database.py`: database-related custom exception classes;
- `http.py`: custom HTTP exceptions;
- `handlers.py`: FastAPI exception handlers that map exceptions to API responses.

`app/utils`:

Provides utility functions, helpers, and abstractions for cross-cutting concerns.

- `cache.py`: Redis client setup for caching and session management;
- `constants.py`: application-wide constants;
- `misc.py`: general-purpose helper functions;
- `mixins.py`: mixin classes for extending Pydantic models;
- `pagination.py`: utilities for pagination handling;
- `secrets.py`: secret management utilities (e.g., API keys, credentials);
- `tokens.py`: JWT token generation and validation;
- `types.py`: shared type hints and definitions.

`app/settings.py`:

Handles application configuration (e.g., environment variables, settings management).

`app/main.py`:

The FastAPI application instance setup, including routers registration and startup events.

Project root:

- `dev.Dockerfile` / `prod.Dockerfile`: separate Dockerfiles for development and production environments;
- `dev.docker-compose.yml` / `prod.docker-compose.yml`: Docker Compose configurations for spinning up development and production environments;
- `pyproject.toml`: project dependencies and configuration using the UV package manager;
- `uv.lock`: lockfile for exact dependency versions;
- `entrypoint.sh`: entrypoint script used when the application runs inside a Docker container;
- `README.md`: overview and documentation for setting up and running the project.

### 🌳 Project Tree

```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── alembic.ini
│   ├── database
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── migrations
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions
│   │   │       └── 2025_04_06_...
│   │   └── models.py
│   ├── entrypoint.sh
│   ├── exceptions
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── handlers.py
│   │   └── http.py
│   ├── main.py
│   ├── manager
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── repository
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── misc.py
│   │   └── user.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── settings.py
│   └── utils
│       ├── __init__.py
│       ├── cache.py
│       ├── constants.py
│       ├── misc.py
│       ├── mixins.py
│       ├── pagination.py
│       ├── secrets.py
│       ├── tokens.py
│       └── types.py
├── dev.Dockerfile
├── dev.docker-compose.yml
├── prod.Dockerfile
├── prod.docker-compose.yml
├── pyproject.toml
└── uv.lock
```
