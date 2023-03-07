from bs4 import BeautifulSoup
import requests
import unicodedata
from langdetect import detect
import pandas as pd
import customExeptions as cex
from flask_sqlalchemy import SQLAlchemy


class Parser:
    HEADER: dict[str: str] = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    
    def __init__(self, url):
        self.url = url
        self.parsedPage = self.bs4Parse()
    
    def makeRequest(self) -> requests:
        try:
            response = requests.get(self.url, headers=self.HEADER)
        except:
            raise cex.RequestExeption
        else:
            if response.status_code == 200:
                return response
            else:
                return None
        
    def bs4Parse(self) -> BeautifulSoup:
        response = self.makeRequest()
        try:
            parserPage: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        except:
            raise cex.ParserExeption
        else:
            return parserPage

    def getHeader(self):
        header: str = self.parsedPage.find('title').get_text()
        return header
    
    def getLinks(self) -> list[str]:
        urls: list = []
        for link in self.parsedPage.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                urls.append(href)
        links: list[str]  = list(set(urls))
        return links
    
    def getParagraphs(self) -> list[str]:
        pr: list = []
        for pTag in self.parsedPage.find_all('p'):
            if pTag:
                try:
                    text = pTag.text
                    pTag = text.replace("\n", "")
                    pTag = unicodedata.normalize('NFKD', pTag)  # delete \xa0
                except:
                    pass
                else:
                    pr.append(pTag)
        return list(set(pr))

    def detectLanguage(self, paragraphs) -> list[str]:
        lang: list = []
        for p in paragraphs:
            try:
                lang.append(detect(p))
            except:
                lang.append(None)
        return lang

    def convertToCSV(self, header, links, paragraphs, lang):
        try:
            df = pd.DataFrame({'URL': pd.Series(self.url), 'Header': pd.Series(header), 'Paragraph': pd.Series(paragraphs), 'Links': pd.Series(links), 'Language': pd.Series(lang)})
            csvData = df.to_csv(index=False, encoding="utf-8")
        except:
            raise cex.ConvertToCSVExeption
        else:
            return csvData

    def csvFile(self):
        header = self.getHeader()
        links = self.getLinks()
        paragraphs = self.getParagraphs()
        lang = self.detectLanguage(paragraphs)
        csvData = self.convertToCSV(header, links, paragraphs, lang)
        return csvData