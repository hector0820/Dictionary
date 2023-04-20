class FindMeaning():
    def __init__(self, word):
        self.word = word
        self.urls = {"Spanish": 'https://www.collinsdictionary.com/dictionary/english-spanish/{}'.format(self.word),
                     "English": 'https://www.collinsdictionary.com/dictionary/english/{}'.format(word)}
        self.EnglishPage = None
        self.SpanishPage = None
        self.definitions = None

        self.meaning = None
        self.traduction = None
        self.examples = None
        self.ejemplos = None

    def WebScrap(self):
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }
        try:
            import requests
            self.EnglishPage = requests.get(self.urls['English'], headers=headers).content 
            self.SpanishPage = requests.get(self.urls['Spanish'], headers=headers).content 
        except:
            return "Check your internet connection"

    def Definitions(self):
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(self.SpanishPage, 'html.parser')
        self.traduction = soup.find_all("a", {"class": ["quote", "ref"]})[0].text
        soup = soup.find_all("div", {"class": ["cit", "type-example"]})
        examples = []
        for i in soup:
            for j in i.find_all("span", {"class": ['quote']}):
                examples.append(j.text)

        self.examples = [ examples[0] , examples[2] ]
        self.ejemplos = [ examples[1] , examples[3] ]
        
        ### English
        soup = BeautifulSoup(self.EnglishPage, 'html.parser')
        soup = soup.find("div", {"class": ["content", "definitions", "cobuild", "br"]})
        soup = soup.find_all("div", {"class": ["def"]})
        self.meaning = [re.sub('\n', '', i.text) for i in soup]

    def __repr__(self) -> str:
        return "FindMeaning"
    
    def Finding(self):
        self.WebScrap()
        self.Definitions()