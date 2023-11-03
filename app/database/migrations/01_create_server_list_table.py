from app.database.adapter import Sqlite3Adapter

# Connect to the database using Sqlite3Adapter class
db = Sqlite3Adapter("app/database/dev.db")

# Define the SQL query for creating the new table
# Default image url is app/assets/images/server.png
create_table_query = """
CREATE TABLE IF NOT EXISTS server_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_name TEXT NOT NULL,
    game_name TEXT NOT NULL,
    server_description TEXT,
    ip_address TEXT NOT NULL,
    port INTEGER NOT NULL,
    image_url TEXT NOT NULL DEFAULT './app/assets/images/server.png'
);
"""

# Execute the query
db.execute(create_table_query)

print("Migration completed successfully.")
