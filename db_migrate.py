import os
import sqlite3
from app.database.adapter import Sqlite3Adapter

# Connect to the database using the Sqlite3Adapter class
db = Sqlite3Adapter("app/database/dev.db")

# Get all migration files that end with '.py'
migrations = [f for f in os.listdir("app/database/migrations") if f.endswith(".py")]
migrations.sort()

ran_migrations = []

# Get all migration files that have already been run
# If the migrations table doesn't exist, create it
try:
    ran_migrations = [record[1] for record in db.fetch("SELECT * FROM migrations")]
except:
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        migration TEXT NOT NULL
    );
    """
    )

# Get all migration files that have not been run
unran_migrations = [
    migration for migration in migrations if migration not in ran_migrations
]

# Run all migrations that have not been run
for migration in unran_migrations:
    print(f"Running migration: {migration}")
    exec(open(f"app/database/migrations/{migration}").read())
    db.execute(f"INSERT INTO migrations (migration) VALUES ('{migration}')")

# Close the connection
db.close()

print("All migrations completed successfully.")
