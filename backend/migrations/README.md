# Database Migrations Guide
Execute migrations:
```bash
alembic upgrade head
alembic downgrade -1
```
All downgrades must be idempotent and non-destructive to audit tables.
