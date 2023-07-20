import os
import sys
import re
import sqlite3

class DataBase():
    def __init__(self):
        self.word = None
        self.data = {"word": self.word, "translation": None, "meaning": None }
        self.cursor = None
        self.connection = None
        self.id = None

        self.DataBase()

    def DataBase(self):
        if os.path.exists('words.sqlite3'):
            self.connection = sqlite3.connect('words.sqlite3')
            self.cursor = self.connection.cursor()
        else:
            self.connection = sqlite3.connect('words.sqlite3')
            self.cursor = self.connection.cursor()
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
                ''')
            self.connection.commit()

    def Word_in_DataBase(self):
        self.cursor.execute('SELECT id FROM Words WHERE word = ? ', (self.word, ))
        id = self.cursor.fetchone()
        if id != None: 
            self.id = id[0]
            self.data['word'] = self.word
        
    def Delete(self):
        words = self.WordsList()
        word = re.sub('\n', '', os.popen('echo "{}" | dmenu'.format("\n".join(words))).read()).lower()
        self.cursor.execute('DELETE FROM Words WHERE word = ?', (word, ))
        self.connection.commit()

    def Adding(self, data):
        self.cursor.execute('INSERT OR IGNORE INTO Words (word) VALUES ( ? )', ( self.word, ))
        self.Word_in_DataBase()

        for i in data['translation']:
            self.cursor.execute('INSERT OR IGNORE INTO Translation (word_id, traduccion) VALUES (?, ? )', (self.id, i))

        for i in data['meaning']:
            self.cursor.execute('INSERT OR IGNORE INTO Meanings (word_id, meaning) VALUES (?, ?)', (self.id, i))

        self.connection.commit()

    def WordsList(self):
        self.cursor.execute('SELECT word FROM Words')
        return [ n[0] for n in self.cursor.fetchall() ]

    def Update(self):
        words = self.WordsList()
        word = re.sub('\n', '', os.popen('echo "{}" | dmenu'.format("\n".join(words))).read()).lower()
        new_word = re.sub('\n', '', os.popen('echo '' | dmenu -p "{}"'.format(word)).read()).lower()

        self.cursor.execute('UPDATE Words SET word = ( ? ) WHERE word = ( ? )', (new_word, word))

        self.word = new_word
        self.data['word'] = new_word
        self.connection.commit()
        self.Word_in_DataBase()

    def Retrieve(self):
        self.cursor.execute('SELECT traduccion FROM Translation WHERE word_id = ? ', (self.id, ))
        self.data['translation'] = [ n[0] for n in self.cursor.fetchall() ]
        
        self.cursor.execute('SELECT meaning FROM Meanings WHERE word_id = ? ', (self.id, ))
        self.data['meaning'] = [ str(n[0]) for n in self.cursor.fetchall() ]

        self.cursor.close()