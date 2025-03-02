

# TASKS.
  - [x] Develop a web application following the MVC design pattern.
    - [x] Implement separate levels for Routing, Business Logic, and DB calls.
    - [x] Added Dependency Inversion (not on the task)
  - [x] Use Python and FastAPI for building the application.
  - [x] Interface with a MySQL database using SQLAlchemy for ORM.
    - [x] Use `asyncmy` since async is generally faster (I mean for most cases that are highly IO bound operations)
  - [x] Implement field validation and dependency injection as needed.


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
  
  - [ ] **AddPost Endpoint**
    - [ ] Accept `text` and a `token` for authentication.
    - [ ] Validate payload size (limit to 1 MB).
    - [ ] Save the post in memory.
    - [ ] Return `postID`.
    - [ ] Return an error for invalid or missing token.
    - [ ] Use dependency injection for token authentication.
  
  - [ ] **GetPosts Endpoint**
    - [ ] Require a token for authentication.
    - [ ] Return all posts for the authenticated user.
    - [ ] Implement response caching for up to 5 minutes for the same user.
    - [ ] Return an error for invalid or missing token.
    - [ ] Use dependency injection for token authentication.
  
  - [ ] **DeletePost Endpoint**
    - [ ] Accept `postID` and a `token` for authentication.
    - [ ] Delete the corresponding post from memory.
    - [ ] Return an error for invalid or missing token.
    - [ ] Use dependency injection for token authentication.

- [ ] **Additional Requirements**
  - [ ] Utilize token-based authentication for "AddPost" and "GetPosts" endpoints, obtainable from the "Login" endpoint.
  - [ ] Implement request validation for "AddPost" to ensure the payload does not exceed 1 MB.
  - [ ] Use in-memory caching for "GetPosts" to cache data for up to 5 minutes.
  - [ ] Ensure extensive type validation in both SQLAlchemy and Pydantic models for every endpoint.
  - [ ] Optimize all functions and dependencies to avoid redundant DB calls or logic.
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
