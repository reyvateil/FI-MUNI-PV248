import re # regular expressions
import sqlite3

# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).

class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if ( self.id is None ):
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.name = re.sub('\([0-9/+-]+\)', '', string).strip()
        m = re.search('([0-9]+)--([0-9]+)', string)
        if m is not None:
            self.born = int(m.group(1))
            self.died = int(m.group(2))
        else:
            self.born = None
            self.died = None

    def fetch_id( self ):
        self.cursor.execute( "select id, born, died from person where name = ?", (self.name,) )
        res = self.cursor.fetchone()
        if res is not None:
            if (self.born is not None and res[1] is None) or (self.died is not None and res[2] is None):
                self.cursor.execute("UPDATE person SET born = ?, died = ? WHERE id = ?", (self.born, self.died, res[0]))
                print("{} updated with years".format(self.name))
            self.id = res[0]

    def do_store( self ):
        self.cursor.execute( "insert into person (born, died, name) values (?, ?, ?)", (self.born, self.died, self.name) )
        print("{} ({} - {}) saved".format(self.name, self.born, self.died))

conn = sqlite3.connect("scorelib.sqlite")
cur = conn.cursor()

def process_composer(line_regex):
    key, val = line_regex.groups()
    if key.lower() == 'composer':
        composers = val.split(';')
        for composer in composers:
            Person(conn, composer.strip()).store()

with open("C:\\Users\\reyvateil\\Documents\\PythonKurz\\scorelib.txt", encoding="utf-8", mode='r') as f:
    rg = re.compile("(.*): (.*)")
    for line in f:
        m = rg.match(line)
        if m is None:
            continue

        process_composer(m)
        conn.commit()

cur.execute("SELECT count(*) FROM person;")
conn.commit()
