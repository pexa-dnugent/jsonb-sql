from psycopg.errors import DuplicateObject
from dbscripts.dblib import pg_connect, pg_db_info

db = pg_db_info()
pg = pg_connect(db)

try:
    pg.execute("""\
    CREATE TYPE ENTITY_TYPE AS ENUM ('individual', 'organisation')
""")
except DuplicateObject:
    pass

# create
pg.execute("""\
ALTER TABLE persons
  ADD COLUMN IF NOT EXISTS entity_type ENTITY_TYPE DEFAULT 'individual',
  ADD COLUMN IF NOT EXISTS detail JSONB
""")

pg.execute("""\
UPDATE persons
   SET detail = jsonb_build_object('surname', surname, 'firstname', firstname)
   WHERE true
""")

pg.execute("""\
ALTER TABLE persons
  DROP COLUMN firstname,
  DROP COLUMN surname
""")

pg.close()
