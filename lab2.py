from pathlib import Path
import csv

import psycopg2
from psycopg2 import sql, OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if __name__ == '__main__':
    db_name = 'lab2'
    table_name = 'words'
    create = False
    insert = False
    data_path = Path('/opt/lab1/data/docs.csv')
    
    try:
        conn = psycopg2.connect(user='postgres', password='postgres', host='localhost')    
    except OperationalError as e:
        print('Could not connect, creating the database instead')
        conn = psycopg2.connect(user='postgres', password='postgres', host='localhost')
        create = True
        
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    if (create):
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_name))
        )
        print(f'Successfully created database {db_name}')
    
    # https://stackoverflow.com/questions/10598002/how-do-i-get-tables-in-postgres-using-psycopg2
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    tables = cursor.fetchall()
    tables = {t[0] for t in tables} 
    
    if (table_name not in tables):
        print(f'Could not find {table_name} in {db_name} database, creating it')
        cursor.execute(sql.SQL("CREATE TABLE {} (word_name varchar PRIMARY KEY, count integer);").format(
                sql.Identifier(table_name))
            )
        
    if (insert):
        with open(data_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(reader):
                if (i == 0):
                    continue

                cursor.execute("INSERT INTO words (word_name, count) VALUES (%s, %s)", row)

    cursor.execute("SELECT * FROM words")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f'word_name: {row[0]}, count: {row[1]}')
    
