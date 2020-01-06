# The script, create_tables.py, runs in the terminal without errors.
# The script successfully
#   connects to the Sparkify database,
#   drops any tables if they exist,
#   and creates the tables.

import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    # connect to default database
    # connection_string = "host=127.0.0.1 dbname=studentdb user=student password=student"
    connection_string_studentdb = "host=172.17.0.2 dbname=studentdb user=student password=student"
    conn = psycopg2.connect(connection_string_studentdb)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute(
        "CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    #connection_string = "host=127.0.0.1 dbname=sparkifydb user=student password=student"
    connection_string_sparkifydb = "host=172.17.0.2 dbname=sparkifydb user=student password=student"
    conn = psycopg2.connect(connection_string_sparkifydb)
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
