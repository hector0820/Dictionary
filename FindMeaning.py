import re
import requests
from bs4 import BeautifulSoup

class FindMeaning():
    def __init__(self, word) -> str:
        self.word = word.lower()
        self.data = { "word": self.word, "translation": None, "meaning": None }
        self.urls = {"Spanish": 'https://www.collinsdictionary.com/dictionary/english-spanish/{}'.format(self.word),
                     "English": 'https://www.collinsdictionary.com/dictionary/english/{}'.format(self.word) }
        self.pages = {"English": None,
                      "Spanish": None }
        self.status = True
        self.Find()

    def Find(self):
        self.WebScrap()
        if self.status == True:
            self.Translation()
            self.Definitions()

    def WebScrap(self):
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }
        try:
            self.pages["English"] = requests.get(self.urls['English'], headers=headers).content 
            self.pages["Spanish"] = requests.get(self.urls['Spanish'], headers=headers).content 
        except:
            self.status = False

    def Translation(self): 
        soup = BeautifulSoup(self.pages['Spanish'], 'html.parser')
        self.data["translation"] = [ i.text for i in soup.find_all('a', {'class': ['quote', 'ref']}) ][:4]

    def Definitions(self):
        soup = BeautifulSoup(self.pages["English"], 'html.parser')
        div = soup.find("div", {"class": ["content", "definitions", "cobuild", "br"]})
        soup = div.find_all("div", {"class": ["def"]})
        self.data["meaning"] = [ re.sub('\n', '', i.text) for i in soup ]
    
    def __repr__(self) -> str:
        return "FindMeaning"