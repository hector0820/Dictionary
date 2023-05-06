class DataBase():
    def __init__(self, word, obj):
        self.word = word
        self.data = {"word": self.word,
                     "translation": None,
                     "meaning": None,
                     "sentences": None}
        self.cursor = 'hola'
        self.connection = None
        self.obj = obj(word)

        self.Connection()
        self.Create()
        self.Exist()

    def Connection(self):
        import os
        import sqlite3
        if not os.path.exists('words.sqlite3'):
            self.connection = sqlite3.connect('words.sqlite3')
            self.cursor = self.connection.cursor()
            self.Create()
        else:
            self.connection = sqlite3.connect('words.sqlite3')
            self.cursor = self.connection.cursor()

    def Create(self):
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
                example     TEXT  UNIQUE
            );
            CREATE TABLE IF NOT EXISTS Ejemplos (
                id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                word_id     INTEGER,
                example_id  INTEGER,
                traduccion  TEXT  UNIQUE
            );
            ''')
        self.connection.commit()

    def Word_id(self):
        self.cursor.execute('SELECT id FROM Words WHERE word = ? ', (self.word, ))
        return self.cursor.fetchone()[0]
    
    def Exist(self):
        if bool(self.cursor.execute('SELECT * FROM Words WHERE word = ?', ( self.word, )).fetchall()):
            self.Retrieve()
            self.cursor.close()
        else:
            self.obj.Find()
            self.data = self.obj.data
            self.Adding()

    def Retrieve(self):
        word_id = self.Word_id()
        self.cursor.execute('SELECT traduccion FROM Translation WHERE word_id = ? ', (word_id, ))
        translation = [ n[0] for n in self.cursor.fetchall() ]
        
        self.cursor.execute('SELECT meaning FROM Meanings WHERE word_id = ? ', (word_id, ))
        meaning = [ str(n[0]) for n in self.cursor.fetchall() ]

        self.cursor.execute('SELECT example FROM Examples WHERE word_id = ? ', (word_id, ))
        examples = [ str(n[0]) for n in self.cursor.fetchall() ]

        self.data['translation'] = translation
        self.data['meaning'] = meaning

        sentences = dict()
        
        for x in examples:
            self.cursor.execute('SELECT id FROM Examples WHERE example = ? ', (x, ))
            example_id = self.cursor.fetchone()[0]

            self.cursor.execute('SELECT traduccion FROM Ejemplos WHERE example_id = ? ', (example_id, ))
            ejemplos = [ str(n[0]) for n in self.cursor.fetchall() ][0]

            sentences[x] = ejemplos
        
        self.data['sentences'] = sentences

    def AddWord(self):
        self.cursor.execute('INSERT OR IGNORE INTO Words (word) VALUES ( ? )', ( self.word, ))
        return self.Word_id()

    def AddTranslation(self, word_id):
        for i in self.data['translation']:
            self.cursor.execute('INSERT OR IGNORE INTO Translation (word_id, traduccion) VALUES (?, ? )', (word_id, i))

    def AddMeaning(self, word_id):
        for i in self.data['meaning']:
            self.cursor.execute('INSERT OR IGNORE INTO Meanings (word_id, meaning) VALUES (?, ?)', (word_id, i))

    def AddExamples(self, word_id):
        for i,j in self.data['sentences'].items():
            self.cursor.execute('INSERT OR IGNORE INTO Examples (word_id, Example) VALUES (?, ?)', (word_id, i))
            self.cursor.execute('SELECT id FROM Examples WHERE Example = ? ', (i, ))
            example_id = self.cursor.fetchone()[0]
            if type(j) == list:
                for q in j:
                    self.cursor.execute('INSERT OR IGNORE INTO Ejemplos (word_id, example_id, traduccion) VALUES (?, ?, ?)', (word_id, example_id, q))
            else: 
                self.cursor.execute('INSERT OR IGNORE INTO Ejemplos (word_id, example_id, traduccion) VALUES (?, ?, ?)', (word_id, example_id, j))

    def Adding(self):
        word_id = self.AddWord()
        self.AddTranslation(word_id)
        self.AddMeaning(word_id)
        self.AddExamples(word_id)
        self.connection.commit()
        self.cursor.close()