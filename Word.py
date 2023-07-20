import os 
import re
import sqlite3

def Word():
    query = 'xclip -out -selection primary | xclip -in -selection clipboard'
    clip = os.system(query)
    clip = os.popen('xclip -o -selection clipboard').read().lower()
    clip = re.sub('^\s+', '', clip)
    clip = re.sub('^([A-Za-z]+)\s.*', r'\1', clip)
    return clip

def Dmenu(words):
    return re.sub('\n', '', os.popen('echo "{}" | dmenu'.format("\n".join(words))).read()).lower()

def Notifications(database):
    if not len(database['translation']) < 1:
        translations = 'Translation:\n\n' + "".join(list(map(lambda x: ' - ' + x + '\n', database['translation'])))
    else:
        translations = " "
    meaning = 'Meaning:\n\n' + "".join(list(map(lambda x: ' - ' + x + '\n', database['meaning'])))
    query = 'zenity --info --title="{}" --text="{}\n{}" --width=20'.format(database['word'].upper(), translations, meaning)
    os.system(query)