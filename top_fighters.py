from bs4 import BeautifulSoup
import lxml
import requests
import json
import re
import sys


def get_top_fighters(weight_class):
    url = f'https://www.ufc.com/rankings'
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, 'lxml')
    content_divs = soup.find_all('div', class_='view-grouping')
    names = []
    
    for div in content_divs:
        if weight_class in div.text:
            desired_div = div
            a_tag = div.find('a')
            if a_tag:
                names.append(a_tag.text)

    td_elements = desired_div.find_all('td', class_='views-field views-field-title')
    for td in td_elements:
        names.append(td.get_text(strip=True))

    return names

print(get_top_fighters('Middleweight'))
