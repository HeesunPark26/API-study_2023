import sqlite3
import os

def create_connection(db_name):
    """
    Create a database connection to a SQLite database
    SQLite automatically creates the new database when you connect to an SQLite database that does not exist
    
    References
    * https://www.sqlitetutorial.net/sqlite-python/creating-database/
    
    Parameters
    ----------
    db_name: str
        the name of database (with entire path if needed) that you will create
        
    Returns
    -------
    None, database with `db_name` will be created.
    """
    # check if there is a database with `db_name`
    if os.path.exists(db_name):
        print(f"ERROR: '{db_name}' already exists.")
        return

    connection = None
    try: 
        # opens a connection to an SQLite database.
        # connection is `Connection` object that represents the database
        connection = sqlite3.connect(db_name)
        print(f"'{db_name}' was created successfuly (sqlite3 {sqlite3.version}).")
    except sqlite3.Error as e: # If an error occurs when connecting to SQLite DB.
        print(e)
    finally: 
        # close connection
        if connection:
            with open('db_schema.sql') as f:
                connection.executescript(f.read())
            connection.commit()
            connection.close()

# run! 
if __name__ == '__main__':
    create_connection('database.db')
