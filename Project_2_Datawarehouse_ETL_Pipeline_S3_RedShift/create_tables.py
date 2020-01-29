import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    drops all tables

    reads drop queries defined for each table in the list object and 
    executes drop process one table at a time

    Arguments:
    1 - Cur: cursor object to target database connection
    2 - Conn: target database connection object.

    Returns:
    None
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    creates all tables

    reads create queries defined for each table in the list object and 
    executes create process one table at a time

    Arguments:
    1 - Cur: cursor object to target database connection
    2 - Conn: target database connection object.

    Returns:
    None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    main()