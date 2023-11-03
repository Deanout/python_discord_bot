# A model for the server_list table.
# Path: app/models/server_list.py

from app.database.adapter import Sqlite3Adapter


# This should support database operations for the server_list table.
# Operations include: Create, Read, Update, Delete
class ServerList:
    def __init__(self, database=None):
        if database is None:
            # Create the db adapter
            self.db = Sqlite3Adapter("app/database/dev.db")
        else:
            self.db = database

    def create(
        self,
        server_name,
        game_name,
        ip_address,
        port,
        server_description=None,
        image_url=None,
    ):
        self.db.execute(
            f"""
            INSERT INTO server_list (server_name, game_name, server_description, ip_address, port, image_url)
            VALUES ('{server_name}', '{game_name}', '{server_description}', '{ip_address}', '{port}', '{image_url}');
            """
        )
        # Log the creation of the server.
        print(f"Created server: {server_name}")

    def find(self, name=None, game_name=None, ip_address=None, port=None, id=None):
        result = None
        if id is not None:
            # Log out the id
            print(f"Searching for server with id: {id}")
            result = self.db.fetch(
                f"""
            SELECT * FROM server_list WHERE id = '{id}';
            """
            )
        elif name is not None:
            result = self.db.fetch(
                f"""
            SELECT * FROM server_list WHERE server_name = '{name}';
            """
            )
        elif game_name is not None:
            result = self.db.fetch(
                f"""
            SELECT * FROM server_list WHERE game_name = '{game_name}';
            """
            )
        elif ip_address is not None:
            result = self.db.fetch(
                f"""
            SELECT * FROM server_list WHERE ip_address = '{ip_address}';
            """
            )
        elif port is not None:
            result = self.db.fetch(
                f"""
            SELECT * FROM server_list WHERE port = '{port}';
            """
            )
        else:
            result = self.db.fetch(
                """
            SELECT * FROM server_list;
            """
            )

        # If we didn't find anything, return None
        if len(result) == 0:
            print(f"Failed to find server.")
            return None

        result = result[0]
        print(f"Found server: {result}")
        return result

    def all(self):
        return self.db.fetch(
            """
        SELECT * FROM server_list;
        """
        )

    def update(self, server_name, game_name, ip_address, port, server_description=None):
        self.db.execute(
            f"""
        UPDATE server_list
        SET server_name = '{server_name}', game_name = '{game_name}', server_description = '{server_description}', ip_address = '{ip_address}', port = '{port}'
        WHERE server_name = '{server_name}';
        """
        )

    def delete(self, server_id):
        self.db.execute(
            f"""
        DELETE FROM server_list WHERE id = '{server_id}';
        """
        )
        # Log the deletion of the server.
        print(f"Deleted server: {server_id}")
