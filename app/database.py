import os
from pathlib import Path

from peewee import DatabaseProxy, Model, PostgresqlDatabase
from playhouse.db_url import connect

db = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db


def init_db(app):
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        database = connect(database_url)
    elif os.environ.get("DATABASE_HOST") or os.environ.get("DATABASE_NAME"):
        database = PostgresqlDatabase(
            os.environ.get("DATABASE_NAME", "hackathon_db"),
            host=os.environ.get("DATABASE_HOST", "localhost"),
            port=int(os.environ.get("DATABASE_PORT", 5432)),
            user=os.environ.get("DATABASE_USER", "postgres"),
            password=os.environ.get("DATABASE_PASSWORD", "postgres"),
        )
    else:
        database = connect(f"sqlite:///{Path.cwd() / 'local.db'}")
    db.initialize(database)

    @app.before_request
    def _db_connect():
        db.connect(reuse_if_open=True)

    @app.teardown_appcontext
    def _db_close(exc):
        if not db.is_closed():
            db.close()


def create_tables():
    from app.models import Event, Link, User

    db.connect(reuse_if_open=True)
    db.create_tables([User, Link, Event], safe=True)
    ensure_schema()


def ensure_schema():
    ensure_nullable_integer_column("link", "source_id")
    ensure_nullable_integer_column("event", "source_id")
    ensure_unique_index("link_source_id_uq", "link", "source_id")
    ensure_unique_index("event_source_id_uq", "event", "source_id")


def ensure_nullable_integer_column(table_name, column_name):
    if table_name not in db.get_tables():
        return

    existing_columns = {column.name for column in db.get_columns(table_name)}
    if column_name in existing_columns:
        return

    db.execute_sql(f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER")


def ensure_unique_index(index_name, table_name, column_name):
    if table_name not in db.get_tables():
        return

    existing_columns = {column.name for column in db.get_columns(table_name)}
    if column_name not in existing_columns:
        return

    db.execute_sql(
        f"CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name})"
    )
