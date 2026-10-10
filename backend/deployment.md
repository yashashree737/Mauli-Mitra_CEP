### Deployment / commit instructions

Whenever making any commits to the app, deploy to "dev" branch only.
Run the following commands:

If you happen to update data models:
1. Making migrations: `alembic revision --autogenerate -m "add status field"`
2. Applying Migrations: `alembic upgrade head`
This might cause small errors due to PostGIS. In that case, read the migration file generated in `alembic/versions/`; delete the lines causing errors.

General:
1. Updating requirements.txt: `pip free > requirements.txt`
2. Remove any hardcoded secret tokens used in the code, use environment variables.