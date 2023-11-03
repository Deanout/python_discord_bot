# Creates the migrations table in the database if it doesn't exist
from app.database.adapter import Sqlite3Adapter

db = Sqlite3Adapter("app/database/dev.db")

if len(db.fetch("SELECT * FROM migrations")) == 0:
    db.execute(
        """
  CREATE TABLE IF NOT EXISTS migrations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      migration TEXT NOT NULL
  );
  """
    )

print("Migration completed successfully.")
