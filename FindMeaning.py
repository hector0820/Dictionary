class FindMeaning():
    def __init__(self, word):
        self.word = None
        self.data = {"word": None,
                     "translation": None,
                     "meaning": None,
                     "sentences": None}
        self.urls = {"Spanish": 'https://www.collinsdictionary.com/dictionary/english-spanish/{}'.format(self.word),
                     "English": 'https://www.collinsdictionary.com/dictionary/english/{}'.format(word) }
        self.pages = {"English": None,
                      "Spanish": None }

    def Find(self):
        self.WebScrap()
        self.Translation()
        self.Definitions()
        self.Examples()

    def WebScrap(self):
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }
        try:
            import requests
            self.pages["English"] = requests.get(self.urls['English'], headers=headers).content 
            self.pages["Spanish"] = requests.get(self.urls['Spanish'], headers=headers).content 
        except:
            self.pages["English"] = "Check your internet connection"
            self.pages["Spanish"] = "Check your internet connection"

    def Translation(self): 
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(self.pages['Spanish'], 'html.parser')
        self.data["translation"] = [i.text for i in soup.find_all('a', {'class': ['quote', 'ref']})][:4]

    def Definitions(self):
        from bs4 import BeautifulSoup
        import re

        soup = BeautifulSoup(self.pages["English"], 'html.parser')
        div = soup.find("div", {"class": ["content", "definitions", "cobuild", "br"]})
        soup = div.find_all("div", {"class": ["def"]})
        self.data["meaning"] = [re.sub('\n', '', i.text) for i in soup]
    
    def Examples(self):
        from bs4 import BeautifulSoup
        import re
        
        soup = BeautifulSoup(self.pages['Spanish'], 'html.parser')
        
        all = soup.find_all("span", {"class": "quote"})
        translation = soup.find_all("span", {"class": "type-translation"})
        
        all = [ re.sub('^\s+', '', i.text) for i in all ]
        translation = [ re.sub('^\s+', '', i.text) for i in translation ]
        
        examples = set(all).difference(set(translation))
        
        sentences = dict()
        
        sense = soup.find_all("div", {"class": "sense"})
        for i in sense:
            all = [re.sub('^\s+', '', j.text) for j in i.find_all("span", {'class': 'quote'})]
            if not all == list() and len(all) > 2:
                indexes = [ all.index(p) for p in list(set(all).intersection(examples)) ]
                indexes.sort()
        
                q = 0
        
                while q+1 < len(indexes):
                
                    sentence = [all[id] for id in range(indexes[q], indexes[q+1])]
                    key = sentence.pop(0)
                    sentences[key] = sentence[0]
                    q +=1
        self.data["sentences"] = sentences

    def __repr__(self) -> str:
        return "FindMeaning"