import sqlite3


def db_get_single(sql, pk) -> sqlite3.Row:
    """Retrieve a single row from a database table

    Args:
        sql (string): SQL string
        pk (int): Primary of item to retrieve

    Returns:
        sqlite3.Row: The row object representing the retrieved row
    """
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(sql, (pk,))
        return db_cursor.fetchone()


def db_get_all(sql, pk) -> list:
    """Retrieve all rows from a database table

    Args:
        sql (string): SQL string

    Returns:
        list: List of sqlite3.Row objects
    """
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        if pk != 0:
            db_cursor.execute(sql, (pk,))
        else:
            db_cursor.execute(sql)
        return db_cursor.fetchall()


def db_delete(sql, pk) -> int:
    """Delete a row from the database

    Args:
        sql (string): SQL string
        pk (int): Primary key of item to delete

    Returns:
        int: Number of rows deleted
    """
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(sql, (pk,))
        return db_cursor.rowcount


def db_create(sql, data_tuple) -> int:
    """Create a row in a database table

    Args:
        sql (string): SQL string
        data_tuple (tuple): Tuple containing all data values to be mapped to parameters in the SQL string

    Returns:
        int: The new id of the created row
    """
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(sql, data_tuple)
        new_id = db_cursor.lastrowid  # integer
        db_cursor.execute("SELECT * FROM orders WHERE id=?", (new_id,))
        return db_cursor.fetchone()
