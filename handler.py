from bs4 import BeautifulSoup
import requests
import unicodedata
from langdetect import detect
import pandas as pd


class Parser:
    HEADER: dict[str: str] = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    
    def __init__(self, url):
        self.url = url
        self.parsedPage = self.bs4Parse()
    
    def makeRequest(self):
        try:
            response = requests.get(self.url, headers=self.HEADER)
        except Exception as e:
            print(f"Something was happen - {e}")
        else:
            return response
        
    def bs4Parse(self):
        response = self.makeRequest()
        parserPage: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        return parserPage

    def getHeader(self):
        header: str = self.parsedPage.find('title').get_text()
        return header
    
    def getLinks(self):
        urls: list[str] = []
        for link in self.parsedPage.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                urls.append(href)
        removeDuplicates = set(urls)
        return list(removeDuplicates)
    
    def getParagraphs(self):
        pr = []
        for pTag in self.parsedPage.find_all('p'):
            if pTag:
                text = pTag.text
                pTag = text.replace("\n", "")
                pTag = unicodedata.normalize('NFKD', pTag)  # delete \xa0
                pr.append(pTag)
        return list(set(pr))

    def detectLanguage(self, paragraphs):
        lang = []
        for i in paragraphs:
            try:
                lang.append(detect(i))
            except:
                lang.append(None)
        return lang

    def convertToCSV(self, header, links, paragraphs, lang):
        df = pd.DataFrame({'URL': pd.Series(self.url), 'Header': pd.Series(header), 'Paragraph': pd.Series(paragraphs), 'Links': pd.Series(links), 'Language': pd.Series(lang)})
        csvData = df.to_csv(index=False)
        return csvData

    def csvFile(self):
        header = self.getHeader()
        links = self.getLinks()
        paragraphs = self.getParagraphs()
        lang = self.detectLanguage(paragraphs)
        csvData = self.convertToCSV(header, links, paragraphs, lang)
        return csvData