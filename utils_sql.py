import sqlite3
import os
def execute_select_query(db_name, query):
    """
    Parameters
    ----------
    db_name: str
        the name of database (with entire path if needed) that you will connect
    query: str
        query that you will execute
        
    Returns
    -------
    output: list
        query output
    """
    # check if there is a database with `db_name`
    if not os.path.exists(db_name):
        print(f"ERROR: '{db_name}' does not exist.")
        return

    connection = None
    try: 
        # opens a connection to an SQLite database.
        connection = sqlite3.connect(db_name)
    except sqlite3.Error as e: # If an error occurs when connecting to SQLite DB.
        print(e)
    finally: 
        if connection:
            cur = connection.cursor()
            cur.execute(query)
            output = [dict((cur.description[i][0], value) \
                    for i, value in enumerate(row)) for row in cur.fetchall()]
            # close connection
            connection.close()
    return output
def execute_commit_query(db_name, query):
    # check if there is a database with `db_name`
    if not os.path.exists(db_name):
        print(f"ERROR: '{db_name}' does not exist.")
        return

    connection = None
    try: 
        # opens a connection to an SQLite database.
        connection = sqlite3.connect(db_name)
    except sqlite3.Error as e: # If an error occurs when connecting to SQLite DB.
        print(e)
    finally: 
        if connection:
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            # close connection
            connection.close()