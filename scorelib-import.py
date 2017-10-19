import re # regular expressions
import sqlite3
from collections import defaultdict
from pprint import pprint

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
        m = re.search('([0-9]+)--([0-9]+)?', string)
        if m is not None:
            self.born = int(m.group(1))
            self.died = int(m.group(2)) if m.group(2) else m.group(2)
        else:
            self.born = None
            self.died = None

    def fetch_id( self ):
        self.cursor.execute( "select id, born, died from person where name = ?", (self.name,) )
        res = self.cursor.fetchone()
        if res is not None:
            if (self.born is not None and res[1] is None) or (self.died is not None and res[2] is None):
                self.cursor.execute("UPDATE person SET born = ?, died = ? WHERE id = ?", (self.born, self.died, res[0]))
            self.id = res[0]


    def do_store( self ):
        self.cursor.execute( "insert into person (born, died, name) values (?, ?, ?)", (self.born, self.died, self.name) )

class Score (DBItem):
    def __init__(self, conn, genre, key, incipit, year):
        super().__init__(conn)
        self.genre = genre
        self.key = key
        self.incipit = incipit
        self.year = year

    def fetch_id( self ):
        self.cursor.execute( "select id from score where genre = ? and key = ? and incipit = ? and year = ?", (self.genre, self.key, self.incipit, self.year) )
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res[0]

    def do_store( self ):
        self.cursor.execute( "insert into score (genre, key, incipit, year) values (?, ?, ?, ?)", (self.genre, self.key, self.incipit, self.year) )

class Edition(DBItem):
    def __init__(self, conn, score_id, edit_name, year):
        super().__init__(conn)
        self.score_id = score_id
        self.edit_name = edit_name
        self.year = year

    def fetch_id(self):
        self.cursor.execute("select id from edition where score = ? and name = ? and year = ?",
                            (self.score_id, self.edit_name, self.year))
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res[0]

    def do_store( self ):
        self.cursor.execute( "insert into edition (score, name, year) values (?, ?, ?)", (self.score_id, self.edit_name, self.year) )

class Score_author(DBItem):
    def __init__(self, conn, name_id, score_id):
        super().__init__(conn)
        self.name_id = name_id
        self.score_id = score_id

    def fetch_id(self):
        self.cursor.execute("select id from score_author where score = ? and composer = ?",
                            (self.score_id, self.name_id))
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res[0]

    def do_store( self ):
        self.cursor.execute( "insert into score_author (score, composer) values (?, ?)", (self.score_id, self.name_id) )

class Print(DBItem):
    def __init__(self, conn, print_id, partiture, edit_id):
        super().__init__(conn)
        self.print_id = print_id
        self.partiture = partiture
        self.edit_id = edit_id

    def fetch_id(self):
        self.cursor.execute("select id from print where partiture = ? and edition = ?",
                            (self.partiture, self.edit_id))
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res[0]

    def do_store( self ):
        self.cursor.execute( "insert into print (id, partiture, edition) values (?, ?, ?)", (self.print_id, self.partiture, self.edit_id) )

class Voice(DBItem):
    def __init__(self, conn, voice_num, score_id, voice_name):
        super().__init__(conn)
        self.voice_num = voice_num
        self.score_id = score_id
        self.voice_name = voice_name

    def fetch_id(self):
        self.cursor.execute("select id from voice where number = ? and score = ?",
                            (self.voice_num, self.score_id))
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res[0]

    def do_store( self ):
        self.cursor.execute( "insert into voice (number, score, name) values (?, ?, ?)", (self.voice_num, self.score_id, self.voice_name) )

class Edition_author(DBItem):
    def __init__(self, conn, edition_id, editor_id):
        super().__init__(conn)
        self.edition_id = edition_id
        self.editor_id = editor_id

    def fetch_id(self):
        self.cursor.execute("select id from edition_author where edition = ? and editor = ?",
                            (self.edition_id, self.editor_id))
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res[0]

    def do_store( self ):
        self.cursor.execute( "insert into edition_author (edition, editor) values (?, ?)", (self.edition_id, self.editor_id) )

conn = sqlite3.connect("scorelib.sqlite")
cur = conn.cursor()

def make_db_entries(conn, entry):
    pprint(entry)

    composers = [Person(conn, composer) for composer in entry['composer'] if composer]
    for composer in composers:
        composer.store()
        print("Composer: '{}'({})".format(composer.name, composer.id))

    editors = [Person(conn, editor) for editor in entry['editor'] if editor]
    for editor in editors:
        editor.store()
        print("Editor: '{}'({})".format(editor.name, editor.id))

    score = Score(conn, entry['genre'][0], entry['key'][0], entry['incipit'][0], entry['composition year'][0])
    score.store()
    print("Score({}): genre:'{}', key='{}', incipit='{}', composition year='{}'".format(score.id, score.genre, score.key, score.incipit, score.year))

    for composer in composers:
        score_author = Score_author(conn, composer.id, score.id)
        score_author.store()
        print("Score author: '{}'({}) Score: {}".format(composer.name, composer.id, score.id))

    voices = [Voice(conn, voice_num, score.id, voice_name) for voice_num, voice_name in entry['voice']]
    for voice in voices:
        voice.store()
        print("Voice {}: '{}' ({})".format(voice.voice_num, voice.voice_name, voice.id))

    edition = Edition(conn, score.id, entry['edition'][0], entry['publication year'][0])
    edition.store()
    print("Edition({}): '{}' {}".format(edition.id, edition.edit_name, edition.year))

    for editor in editors:
        edition_author = Edition_author(conn, edition.id, editor.id)
        edition_author.store()
        print("Edition author: edition ID: {} editor: '{}' ({})".format(edition.id, editor.name, editor.id))

    print_edition = Print(conn, entry['print number'][0], entry['partiture'], edition.id)
    print_edition.store()
    print("Print edition: print number: {}, partiture: '{}', edition ID: {}".format(print_edition.id, print_edition.partiture, print_edition.edit_id))

def process(entry, line_regex):
    key, val = line_regex.groups()
    key = key.strip().lower()
    val = val.strip()
    if key == 'editor':
        entry[key.lower()] = [None]
        editor_re = re.compile(r'((?:\w+\.? ?)(?:\w+\.? )?(?:\w+))(?:, )?(?:continuo(?:: | by ))?((?:\w+\.? ?)(?:\w+))?', re.UNICODE)
        editor_m = editor_re.match(val)
        if editor_m is not None:
            entry[key] = [editor for editor in editor_m.groups() if editor]
    elif key.startswith('voice'):
        voice_re = re.compile('voice ([0-9]+)')
        voice_m = voice_re.match(key)
        if voice_m is not None:
            entry['voice'].append((voice_m.group(1), val))
    elif key == 'partiture':
        if 'partial' in val.lower():
            entry['partiture'] = 'P'
        elif 'yes' in val.lower():
            entry['partiture'] = 'Y'
        elif 'reduction' in val.lower():
            entry['partiture'] = 'R'
        else:
            entry['partiture'] = 'N'
    else:
        res = [item.strip() if item else None for item in val.split(';')]
        entry[key] = res

with open("C:\\Users\\reyvateil\\Documents\\PythonKurz\\scorelib.txt", encoding="utf-8", mode='r') as f:
    rg = re.compile("^(.*?):(.*)$")
    entry = defaultdict(list)
    flag = False
    for line in f:
        m = rg.match(line)
        if m is None:
            if flag:
                make_db_entries(conn, entry)
                entry = {}
                entry['voice'] = []
                flag = False
            continue

        flag = True
        process(entry, m)
        #conn.commit()

cur.execute("SELECT count(*) FROM person;")
conn.commit()
