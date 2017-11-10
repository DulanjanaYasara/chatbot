import sys

import psycopg2

try:
    con = None
    # Initializing of the database
    con = psycopg2.connect("dbname='extracted_entities' user='dulanjana'")
    cur = con.cursor()
    # Removing the initial data
    cur.execute("DROP TABLE IF EXISTS Entities")
    cur.execute("CREATE TABLE Entities(Answered_Entity TEXT, Unanswered TEXT)")

except psycopg2.DatabaseError, e:

    if con:
        con.rollback()
    print 'Initializing Error %s' % e
    sys.exit(1)


def insert_into_psql(answered_entity, unanswered_entity):
    entities = (
        (answered_entity, unanswered_entity),
    )

    try:
        query = "INSERT INTO Entities( Answered_Entity, Unanswered) VALUES (%s, %s)"
        cur.executemany(query, entities)
        con.commit()

    except psycopg2.DatabaseError, e:

        if con:
            con.rollback()

        print 'Error %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()
