import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    populates staging tables

    reads copy command defined for each staging table in the list object and 
    executes copy process one by one

    Arguments:
    1 - Cur: cursor object to target database connection
    2 - Conn: target database connection object.

    Returns:
    None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    populates dimension and fact tables

    reads insert queries defined for each table in the list object and 
    executes inserts process one table at a time

    Arguments:
    1 - Cur: cursor object to target database connection
    2 - Conn: target database connection object.

    Returns:
    None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()