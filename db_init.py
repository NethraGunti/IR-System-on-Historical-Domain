import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('inforet.db')
    print("'inforet' database created successfully!")

    #delete tables if already existing
    q = "drop table if exists DOCTABLE;"
    conn.execute(q)
    q = "drop table if exists TAGSTABLE;"
    conn.execute(q)
    q = "drop table if exists TERMSTABLE;"
    conn.execute(q)
    q = "drop table if exists POSITIONALINDEX;"
    conn.execute(q)
    q = "drop table if exists KEYFIGURESTABLE;"
    conn.execute(q)

    #create new databases
    #KEYFIGURES -> (FIGURESID, FIGURE)
    conn.execute('''CREATE TABLE KEYFIGURESTABLE
    (FIGUREID INTEGER PRIMARY KEY,
    FIGURE      TEXT    NOT NULL)''')
    print("'KEYFIGURESTABLE' table created succssfully!")

    #DOCTABLE -> (DOCID, DOCTITLE, WORDCOUNT, KEYFIGURES)
    #KEYFIGURES = list of foreign keys in string format
    conn.execute('''CREATE TABLE DOCTABLE
    (DOCID          INTEGER PRIMARY KEY,
    DOCTITLE        TEXT    NOT NULL,
    WORDCOUNT       INT     NOT NULL,
    FIGUREID        TEXT    NOT NULL)''')
    print("'DOCTABLE' table created succssfully!")

    #TAGSTABLE -> (TAGID, TAG, DOCIDS)
    #DOCIDS = list of foreign keys in string format
    conn.execute('''CREATE TABLE TAGSTABLE
    (TAGID          INTEGER PRIMARY KEY,
    TAG             TEXT    NOT NULL,
    DOCIDS          TEXT    NOT NULL)''')
    print("'TAGSLIST' table created succssfully!")

    #TERMSTABLE -> (TERMID, TERMTITLE, DOCCOUNT)
    conn.execute('''CREATE TABLE TERMSTABLE
    (TERMID          INTEGER PRIMARY KEY,
    TERM             TEXT    NOT NULL,
    DOCCOUNT         INTEGER NOT NULL)''')
    print("'TERMSTABLE' table created succssfully!")

    #POSITIONALINDEX -> (TERMID, DOCID, POSITIONS, TERMCOUNT)
    conn.execute('''CREATE TABLE POSITIONALINDEX
    (TERMID         INT     PRIMARY KEY,
    DOCID           INT     NOT NULL,
    POSITIONS       TEXT    NOT NULL,
    TERMCOUNT       INT     NOT NULL,
    FOREIGN KEY (DOCID) REFERENCES DOCTABLE (DOCID),
    FOREIGN KEY (TERMID) REFERENCES TERMSTABLE (TERMID))''')
    print("'POSITIONALINDEX' table created succssfully!")
    
