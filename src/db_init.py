import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('inforet.db')
    conn.isolation_level = None
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
    conn.execute('''INSERT INTO KEYFIGURESTABLE(FIGUREID, FIGURE) VALUES(1, 'FIGURE1') ''')
    conn.execute('''INSERT INTO KEYFIGURESTABLE(FIGUREID, FIGURE) VALUES(2, 'FIGURE2') ''')

    #DOCTABLE -> (DOCID, DOCTITLE, WORDCOUNT, KEYFIGURES)
    #KEYFIGURES = list of foreign keys in string format
    conn.execute('''CREATE TABLE DOCTABLE
    (DOCID          INTEGER PRIMARY KEY,
    DOCTITLE        TEXT    NOT NULL,
    WORDCOUNT       INT     NOT NULL,
    KEYFIGUREIDS        TEXT    NOT NULL)''')
    print("'DOCTABLE' table created succssfully!")
    conn.execute('''INSERT INTO DOCTABLE(DOCID, DOCTITLE, WORDCOUNT, KEYFIGUREIDS) VALUES(1, 'DOC TITLE 1', 10, '1, 2') ''')
    conn.execute('''INSERT INTO DOCTABLE(DOCID, DOCTITLE, WORDCOUNT, KEYFIGUREIDS) VALUES(2, 'DOC TITLE 2', 15, '1') ''')

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
    conn.execute('''INSERT INTO TERMSTABLE(TERMID, TERM, DOCCOUNT) VALUES(1, 'one', 2) ''')
    conn.execute('''INSERT INTO TERMSTABLE(TERMID, TERM, DOCCOUNT) VALUES(2, 'two', 1) ''')

    #POSITIONALINDEX -> (TERMID, DOCID, POSITIONS, TERMCOUNT)
    conn.execute('''CREATE TABLE POSITIONALINDEX
    (TERMID         INT     NOT NULL,
    DOCID           INT     NOT NULL,
    POSITIONS       TEXT    NOT NULL,
    TERMCOUNT       INT     NOT NULL,
    FOREIGN KEY (DOCID) REFERENCES DOCTABLE (DOCID),
    FOREIGN KEY (TERMID) REFERENCES TERMSTABLE (TERMID))''')
    print("'POSITIONALINDEX' table created succssfully!")
    conn.execute('''INSERT INTO POSITIONALINDEX(TERMID, DOCID, POSITIONS, TERMCOUNT) VALUES(1, 1, '5, 7, 8', 3) ''')
    conn.execute('''INSERT INTO POSITIONALINDEX(TERMID, DOCID, POSITIONS, TERMCOUNT) VALUES(1, 2, '6', 1) ''')
    conn.execute('''INSERT INTO POSITIONALINDEX(TERMID, DOCID, POSITIONS, TERMCOUNT) VALUES(2, 1, '1,2,3,4,5,6,', 6) ''')
    
