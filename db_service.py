import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app-db', 'guests.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def init():
    """Initialize the guests table if it doesn't exist."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS guests (
                guestId INTEGER PRIMARY KEY,
                name TEXT,
                tlf INTEGER
            )
        ''')


def read_all():
    """Return all guest records."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM guests")
        rows = cur.fetchall()

        if len(rows) == 0:
            return None

        guests = [{"guestId": row[0], "name": row[1], "tlf": row[2]} for row in rows]
    return guests


def read(guest_id):
    """Return a single guest by ID."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM guests WHERE guestId = ?", (guest_id,))
        row = cur.fetchone()

        if row:
            guest = {"guestId": row[0], "name": row[1], "tlf": row[2]}
        else:
            return None
    return guest


def create(guest):
    """Insert a new guest into the guests table."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''
            INSERT INTO guests (guestId, name, tlf)
            VALUES (:guestId, :name, :tlf)
        ''', guest)

        new_guest_id = cur.lastrowid
        con.commit()
    return new_guest_id


def delete(guest_id):
    """Delete a guest by ID."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM guests WHERE guestId = ?", (guest_id,))
        con.commit()

