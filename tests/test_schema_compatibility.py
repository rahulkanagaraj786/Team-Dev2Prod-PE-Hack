import sqlite3

from app import create_app
from app.database import db


def test_create_app_adds_missing_source_id_columns(monkeypatch, tmp_path):
    database_path = tmp_path / "legacy.db"
    connection = sqlite3.connect(database_path)
    connection.executescript(
        """
        CREATE TABLE link (
            id INTEGER PRIMARY KEY,
            slug VARCHAR(32) NOT NULL UNIQUE,
            user_id INTEGER,
            target_url TEXT NOT NULL,
            title VARCHAR(160),
            is_active INTEGER NOT NULL DEFAULT 1,
            visit_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE event (
            id INTEGER PRIMARY KEY,
            link_id INTEGER NOT NULL,
            user_id INTEGER,
            event_type VARCHAR(32) NOT NULL,
            timestamp TEXT NOT NULL,
            details TEXT
        );
        """
    )
    connection.commit()
    connection.close()

    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")

    app = create_app()
    app.config.update(TESTING=True)

    link_columns = {column.name for column in db.get_columns("link")}
    event_columns = {column.name for column in db.get_columns("event")}

    assert "source_id" in link_columns
    assert "source_id" in event_columns

    with app.test_client() as client:
        response = client.get("/urls")

    assert response.status_code == 200
    assert response.get_json() == []

    if not db.is_closed():
        db.close()
