

ON THE TASK IT IS ASKING TO SAVE DATA ON THE MEMORY.
 - I WOULD ASSUME IT MEANS ON THE DATABASE.

# TASKS.

- [ ] DEPLOY it on RENDER
    - DEPLOY IT ON RENDER
- [ ] Write end to wnd and integration tessts including orm mapping tests

  - [x] Develop a web application following the MVC design pattern.
    - [x] Implement separate levels for Routing, Business Logic, and DB calls.
        - I've used DDD for this project where the domains are located inside `app.core.domain`
    - [x] Added Dependency Inversion (not on the task)
  - [x] Use Python and FastAPI for building the application.
  - [x] Interface with a MySQL database using SQLAlchemy for ORM.
    - [x] Use `asyncmy` since async is generally faster (I mean for most cases that are highly IO bound operations)
  - [x] Implement field validation and dependency injection as needed.

- [x] pre-commit configs.
    - [x] setup ruff
    - [x] setup pyright
    - [x] setup mypy

- [x] Exception handling on the services.
- [x] UTILIZE unit of work.
    - the requirement doesn't have a complex business logic that requires a  a unit of work.

- [x] **Data Models**
  - [x] For all data entities, define:
    - [x] A SQLAlchemy model.
    - [x] A Pydantic model with extensive type validation for all fields.

- [x] **Endpoints Implementation**
  - [x] **Signup Endpoint**
    - [x] Accept `email` and `password`.
    - [x] Return a token (JWT or randomly generated string).

  - [x] **Login Endpoint**
    - [x] Accept `email` and `password`.
    - [x] Return a token upon successful login.
    - [x] Return an error response if login fails.

  - [x] **AddPost Endpoint**
    - [x] Accept `text` and a `token` for authentication.
    - [x] Validate payload size (limit to 1 MB).
    - [x] Save the post in memory.
    - [x] Return `postID`.

  - [x] **GetPosts Endpoint**
    - [x] Require a token for authentication.
    - [x] Return all posts for the authenticated user.
    - [x] Implement response caching for up to 5 minutes for the same user.

  - [x] **DeletePost Endpoint**
    - [x] Accept `postID` and a `token` for authentication.
    - [x] Delete the corresponding post from memory.


- `app.api.v1.dependencies.get_current_user` handles the validation for this two steps
    - [x] Return an error for invalid or missing token.
    - [x] Use dependency injection for token authentication.

- [ ] **Additional Requirements**
  - [x] Utilize token-based authentication for "AddPost" and "GetPosts" endpoints, obtainable from the "Login" endpoint.
  - [x] Implement request validation for "AddPost" to ensure the payload does not exceed 1 MB.
  - [x] Use in-memory caching for "GetPosts" to cache data for up to 5 minutes.
  - [x] Ensure extensive type validation in both SQLAlchemy and Pydantic models for every endpoint.
  - [x] Optimize all functions and dependencies to avoid redundant DB calls or logic.
  - [ ] Provide comprehensive documentation and comments on each function, explaining their purpose and functionality.

# create a virtual environment

```bash
uv venv --python=3.12 --seed .venv
```

# Activate environment
```bash
source ./activate_project.sh
```

# add new package to dev
```bash
uv add --dev <PackageName>
```

# add new package to test environment
```bash
uv add --group test <PackageName>
```

# add new package to prod
```bash
uv add <PackageName>
```

# Install Production Package
```bash
uv sync --no-dev
```

# Install dev Package
```bash
uv sync
```

# Install test Package
```bash
uv sync --group test
```



# Migrations

## to use alembic just use `docker compose run --rm alembic <Command>`

* to create a new migration
```
docker compose run --rm alembic revision --autogenerate -m "migration name"
```

# to upgrade the migration
```
docker compose run --rm alembic upgrade +1
```

# to downgrade the migration
```
docker compose run --rm alembic downgrade -1
```


# To start the app on dev branch
```
docker compose up app -d
```


# To create test database
```
docker compose exec db createdb -U root backend-test
```

# To run the tests
```
docker compose run --rm test pytest
```
