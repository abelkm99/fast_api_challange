# FastAPI Challenge Web Application

A robust web application built with Python, FastAPI, and MySQL that demonstrates the use of the MVC design pattern, Domain-Driven Design (DDD), Dependency Injection, and advanced ORM integration with SQLAlchemy.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features and Endpoints](#features-and-endpoints)
- [Setup and Installation](#setup-and-installation)
- [Environment Configuration](#environment-configuration)
- [Development and Deployment](#development-and-deployment)
- [Migrations](#migrations)
- [Testing](#testing)
- [Additional Notes](#additional-notes)
- [Commands Cheat Sheet](#commands-cheat-sheet)

## Overview
This project provides a complete solution for a web application that includes user authentication, post management, and caching. The application leverages asynchronous operations (using `asyncmy` with MySQL), comprehensive type validation with both SQLAlchemy and Pydantic, and follows clean architectural principles.

## Architecture
- **MVC Design Pattern:**  
  - **Routing:** Handles API endpoints.
  - **Business Logic:** Encapsulated in service layers and domain models (located in `app.core.domain`).
  - **Database Access:** Managed via SQLAlchemy ORM.
- **Domain-Driven Design (DDD):** Focuses on modeling the domain and its logic.
- **Dependency Inversion:** Enhances modularity and testability.
- **Token-Based Authentication:** Secures endpoints such as AddPost and GetPosts.
- **Caching:** Implements in-memory caching (up to 5 minutes) for the GetPosts endpoint.

## Features and Endpoints
### User Authentication
- **Signup Endpoint:**
  - Accepts `email` and `password`.
  - Returns a token (JWT or a randomly generated string).
- **Login Endpoint:**
  - Accepts `email` and `password`.
  - Returns a token upon successful login.
  - Provides error responses for failed logins.

### Post Management
- **AddPost Endpoint:**
  - Accepts `text` and an authentication token.
  - Validates that the payload size does not exceed 1 MB.
  - Saves the post in memory.
  - Returns a `postID` upon successful submission.
- **GetPosts Endpoint:**
  - Requires a valid token for authentication.
  - Returns all posts for the authenticated user.
  - Caches responses for up to 5 minutes for repeated requests.
- **DeletePost Endpoint:**
  - Accepts `postID` and an authentication token.
  - Deletes the corresponding post from memory.

### Data Models
For every data entity, the project includes:
- A **SQLAlchemy model** for database interactions.
- A **Pydantic model** with extensive type validation for request payloads.

## Setup and Installation
### Prerequisites
- Python 3.12
- Docker and Docker Compose


## Environment Configuration
Create a `.env` file in your project root with the following settings:
```bash
DEVELOPMENT_DATABASE_URL="mysql+asyncmy://root:123456789@localhost:5444/backend?charset=utf8mb4"
ENVIRONMENT="development"
```

## Development and Deployment
- **Local Development:**  
  Use Docker Compose to start the application:
  ```bash
  docker compose up app -d
  ```
- **Deployment:**  
  The application is deployed on Render:
  - [Render URL](https://fast-api-challange.onrender.com/)
  - [Swagger Documentation](https://fast-api-challange.onrender.com/docs)


### Creating a Virtual Environment
Create and seed a virtual environment using:
```bash
uv venv --python=3.12 --seed .venv
```
Activate the environment:
```bash
source ./activate_project.sh
```

### Managing Dependencies
- **Development Dependencies:**
  ```bash
  uv add --dev <PackageName>
  ```
- **Test Environment Dependencies:**
  ```bash
  uv add --group test <PackageName>
  ```
- **Production Dependencies:**
  ```bash
  uv add <PackageName>
  ```

Install packages as needed:
- **Production:**
  ```bash
  uv sync --no-dev
  ```
- **Development:**
  ```bash
  uv sync
  ```
- **Testing:**
  ```bash
  uv sync --group test
  ```

## Migrations
Alembic is used to handle database migrations.
- **Create a New Migration:**
  ```bash
  docker compose run --rm alembic revision --autogenerate -m "migration name"
  ```
- **Upgrade Migrations:**
  ```bash
  docker compose run --rm alembic upgrade +1
  ```
- **Downgrade Migrations:**
  ```bash
  docker compose run --rm alembic downgrade -1
  ```

## Testing
### Creating a Test Database
```bash
docker compose exec db createdb -U root backend-test
```
### Running Tests
Execute tests with:
```bash
docker compose run --rm test pytest
```
*Note: End-to-end and integration tests, including ORM mapping tests, are pending.*

## Additional Notes
- **Pre-commit Hooks:** Configured with ruff, pyright, and mypy to ensure code quality.
- **Unit of Work:** Utilized in services, though the current business logic is relatively straightforward.
- **Caching Enhancements:** Future work includes improving caching strategies.
- **Further Testing:** End-to-end and integration tests remain as future enhancements.

## Commands Cheat Sheet
- **Activate Virtual Environment:**
  ```bash
  source ./activate_project.sh
  ```
- **Add New Package:**
  - For development:
    ```bash
    uv add --dev <PackageName>
    ```
  - For testing:
    ```bash
    uv add --group test <PackageName>
    ```
  - For production:
    ```bash
    uv add <PackageName>
    ```
- **Sync Packages:**
  - Production:
    ```bash
    uv sync --no-dev
    ```
  - Development:
    ```bash
    uv sync
    ```
  - Testing:
    ```bash
    uv sync --group test
    ```
- **Docker Compose Commands:**
  - Start the app:
    ```bash
    docker compose up app -d
    ```
  - Create test database:
    ```bash
    docker compose exec db createdb -U root backend-test
    ```
  - Run tests:
    ```bash
    docker compose run --rm test pytest
    ```
```
