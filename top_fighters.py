from bs4 import BeautifulSoup
import lxml
import requests
import json
import re
import sys

class UFCRankingScraper:
    def __init__(self) -> None:
        self.url = f'http://www.ufc.com/rankings'
        self.page = None
        self.soup = None
        self.content_divs = None
    
    def fetch_data(self):
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, 'lxml')
        self.content_divs = self.soup.find_all('div', class_='view-grouping')

    def get_top_fighters(self, weight_class):
        names = []

        if not self.content_divs:
            self.fetch_data()

        for div in self.content_divs:
            if weight_class in div.text:
                desired_div = div
                # find the champion of the current division
                a_tag = div.find('a')
                if a_tag:
                    # add the name of the champion into names
                    names.append(a_tag.text)

        # find the rest of the fighters in the division
                td_elements = desired_div.find_all('td', class_='views-field views-field-title')
                for td in td_elements:
            # add the fighters names into the names array
                    names.append(td.get_text(strip=True))

        return names

