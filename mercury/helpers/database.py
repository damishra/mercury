from os import environ


DBHOST = environ.get('DBHOST')
DBPORT = environ.get('DBPORT')
DBUSER = environ.get('DBUSER')
DBPASS = environ.get('DBPASS')
DBNAME = environ.get('DBNAME')

DBURI = f"postgres://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}"
