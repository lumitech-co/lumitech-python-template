# Lumitech Python Backend Template

The API powered by [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/latest/) and [SQLAlchemy](https://www.sqlalchemy.org/).

# Environment Variables

Environment variables are listed in [_.env.example_](.env.example) file.

# Quick Start

- Navigate to the project directory via `cd <project_name>`.
- Copy [_.env.example_](.env.example) to _.env_ file via `cp .env.example .env`.
- Fill environment variables listed in _.env_ with relevant values.
- Create docker network via `docker network create <network_name>`
- Run the project via `docker compose up -f prod.docker-compose.yml up`.

  _NOTE: use `-d` flag to run containers in the background._

# Contribution Guidelines

## Development Environment

- Navigate to the project directory via `cd <project_name>`.
- Create a virtual environment via `python -m venv .venv`.
- Activate the virtual environment via `source .venv/bin/activate`.
- Install the project's dependencies via `pip install -r dev.requirements.txt`.
- Initialize pre-commit environment and install pre-commit hooks via `pre-commit install`.
- Copy [_.env.example_](.env.example) to _.env_ file via `cp .env.example .env`.
- Fill environment variables listed in _.env_ with relevant values.
- Run the project via `docker compose up -f dev.docker-compose.yml up`.

  _NOTE: use `-d` flag to run containers in the background._

## Conventional Commits

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
