import sqlite3
from typing import Any
from contextlib import contextmanager
from .schemas import ShipmentCreate, ShipmentUpdate


class Database:
    def connect_to_db(self):
        # Make the connection with database
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        # Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()
        print("connected to the sqlite.db...")

    def create_table(self):
        # 1. Create a table
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
        """
        )

    def create(self, shipment: ShipmentCreate) -> int:
        # Find a new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1 if result[0] else 1
        # # 2. Add shipment data
        self.cur.execute(
            """
            INSERT INTO shipment
            VALUES (:id, :content, :weight, :status)
        """,
            {"id": new_id, **shipment.model_dump(), "status": "placed"},
        )
        self.conn.commit()

        return new_id

    def get(self, id: int) -> dict[str, Any] | None:
        # 3. Read a shipment by id
        self.cur.execute(
            """
            SELECT * FROM shipment
            WHERE id = ?
        """,
            (id,),
        )
        row = self.cur.fetchone()
        return (
            {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3],
            }
            if row
            else None
        )

    def update(self, id: int, shipment: ShipmentUpdate) -> dict[str, Any] | None:
        self.cur.execute(
            """
            UPDATE shipment SET status = :status
            WHERE id = :id
        """,
            {"id": id, **shipment.model_dump()},
        )
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        # 5. Delete a shipment by id
        self.cur.execute(
            """
            DELETE from shipment 
            WHERE id = :id
        """,
            {"id": id},
        )
        self.conn.commit()

    def close(self):
        # Close the connection when done
        print("...connection closed")
        self.conn.close()

    # def __enter__(self):
    #     print("Enter the context")
    #     self.connect_to_db()
    #     # Create table if not exists
    #     self.create_table()
    #     return self

    # def __exit__(self, *arg):
    #     print("Exiting the context")
    #     self.close()


# Usage
@contextmanager
def managed_db():
    db = Database()
    print("Enter the setup")
    # Setup
    db.connect_to_db()
    db.create_table()

    yield db

    print("exit the context")
    # Dispose
    db.close()


with managed_db() as db:
    print(db.get(0))
    print(db.get(1))
    print(db.get(2))
    print(db.get(3))
    print(db.get(6))
