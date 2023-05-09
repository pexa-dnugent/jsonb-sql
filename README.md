# JSONB

This is a simple project written in python that explores JSONB fields at the SQL level.

## Requirements

- python 3.8 or later

## Installation
- copy or rename .env-example to .env
- add passwords in the appropriate place in .env using a text editor

```shell
# Create and activate a python virtual env
# install flit to help with package management
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -U pip flit
# install dependencies
$ flit install --only-deps
```

### Running

The following scripts create 20000 records in a local/dockerised postgresql database.
The database is exposed on TCP port 15432 to avoid collisions with any running local instance.
It creates a persistent docker volume for data, so is fully restartable without data loss.

Start the database, create the tables and logins etc.

```shell
$ ./db.sh start
$ dbcreate -c
```

Populate the database with fake data

```shell
$ python src/populate.py
```

At this point the database contains a `persons` table consisting of a id, firstname and surname fields.
We now convert these to a jsonb field `detail` and remove the pre-existing first and surname fields.

```shell
$ python src/convert.py
```

To shut down the database:
```shell
$ ./db.sh stop
```

Some examples of SQL commands to access and use the plain key/values in the JSONB field

```postgresql
-- extract jsonb fields in select
select detail -> 'firstname' as firstname, detail -> 'surname' as surname from persons;

-- drop this record type in case it already exists, then recreate
drop type if exists individual;
create type individual as (firstname text, surname text);

-- extract data as individual records
select jsonb_populate_record(null::individual, detail) from persons;

--- simple select with example ordering by jsonb value
select
   detail -> 'firstname',
   detail -> 'surname'
  from persons
 order by detail -> 'surname';
```
