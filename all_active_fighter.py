from bs4 import BeautifulSoup
import lxml
import requests
import json
import re
import sys

class ActiveFighterNameExtractor:
    def __init__(self):
        pass

    def extractName(self):
        counter = 1

        url = "https://www.ufc.com/athletes/all?filters%5B0%5D=status%3A23" 

        response = requests.get(url, params={"page": counter})

        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.find_all("span", class_="c-listing-athlete__name")
        for item in items:
            print(item)
        

        # page = requests.get(url)
        # content=page.text
        # soup = BeautifulSoup(content, 'lxml')
        # names = soup.find_all(class_='c-listing-athlete__name')
            
if __name__ == '__main__':
    print(ActiveFighterNameExtractor().extractName())
