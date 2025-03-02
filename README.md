

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
