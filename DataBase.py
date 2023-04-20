class SQLite3():
    def __init__(self, item):
        import sqlite3
        self.exist = None
        self.cursor = None
        self.connection = None
        self.item = item

        def TestingItem(item):
            if not item.__repr__() == 'FindMeaning':
                return "YOU NEED A 'FindMeaning' OBJECT"
            else:
                self.item = item
                self.word = item.word
                
        
        TestingItem(item)

    def Creating(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Words (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                word    TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Translation (
                id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                word_id     INTEGER,
                traduccion  TEXT  UNIQUE
            );

            CREATE TABLE IF NOT EXISTS Meanings (
                id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                word_id  INTEGER,
                meaning  TEXT
            );

            CREATE TABLE IF NOT EXISTS Examples (
                id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                word_id     INTEGER,
                examples    TEXT  UNIQUE,
                traduccion  TEXT  UNIQUE
            );
            ''')
        self.connection.commit()

    def Connection(self):
        import os
        if not os.path.exists('words.sqlite3'):
            self.connection = sqlite3.connect('words.sqlite3')
            self.cursor = self.connection.cursor()
            self.Creating()
        else:
            self.connection = sqlite3.connect('words.sqlite3')
            self.cursor = self.connection.cursor()
    
    def Exist(self):
        self.exist = bool(self.cursor.execute('SELECT * FROM Words WHERE word = ?', ( self.word, )).fetchall())

    def Adding(self):
        self.cursor.execute('INSERT OR IGNORE INTO Words (word) VALUES ( ? )', ( self.word, ))
        self.cursor.execute('SELECT id FROM Words WHERE word = ? ', (self.word, ))

        word_id = self.cursor.fetchone()[0]

        self.cursor.execute('INSERT OR IGNORE INTO Translation (word_id, traduccion) VALUES (?, ? )', (word_id, self.item.traduction))

        for meanig in self.item.meaning:
            self.cursor.execute('INSERT OR IGNORE INTO Meanings (word_id, meaning) VALUES (?, ?)', (word_id, meanig))
        
        for i, example in enumerate(self.item.examples):
            self.cursor.execute('INSERT OR IGNORE INTO Examples (word_id, examples, traduccion) VALUES (?, ?, ?)',
                                (word_id, example, self.item.ejemplos[i]))

        self.connection.commit()
        self.cursor.close()

    # def Retrieve(self):

    #     if self.exist:
    #         self.cursor.execute('SELECT id FROM Words WHERE word = ? ', (self.word, ))
    #         word_id = self.cursor.fetchone()[0]
    #         self.item.traduction = self.cursor.execute('SELECT traduccion FROM Translation WHERE word_id = ?',(word_id, ) ).fetchone()[0]
    #         self.item.definitions = self.cursor.execute('SELECT meaning FROM Meanings WHERE word_id = ?',(word_id, ) ).fetchall()


    def Finding(self):
        self.Connection()
        
        if not bool(self.exist):
            self.item.Finding()
            self.Adding()