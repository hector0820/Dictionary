import sys
from Word import *
from DataBase import DataBase
from FindMeaning import FindMeaning


if __name__ == '__main__':
    database = DataBase()
    database.word = Dmenu(database.WordsList())
    database.Word_in_DataBase()

    if database.word == '':
        sys.exit()

    match database.word:
        case 'update':
            database.Update()
        case 'delete':
            database.Delete()
            sys.exit()
        case _:
            if database.id == None:
                find_word = FindMeaning(database.word)
                database.Adding(find_word.data)

    database.Retrieve()
    Notifications(database.data)