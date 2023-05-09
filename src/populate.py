from dbscripts.dblib import pg_connect, pg_db_info
from models import create_persons


NROWS = 20000

db = pg_db_info()
pg = pg_connect(db)

pg.execute("""DROP TABLE IF EXISTS persons;""")
pg.execute("""\
CREATE TABLE IF NOT EXISTS persons (
    id UUID NOT NULL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL
)""")

sql = "INSERT INTO persons VALUES" + ",".join(["(%s, %s, %s)" for _ in range(NROWS)])

persons = []
for index, person in enumerate(create_persons(NROWS)):
    if index % 100 == 0:
        print(f"{index}\r", end='', flush=True)
    persons.extend((person.id, person.firstname, person.surname))

pg.execute(sql, persons)

response = pg.execute('SELECT count(*) FROM persons')

print(f"{response.fetchone()[0]} records created")

pg.close()
