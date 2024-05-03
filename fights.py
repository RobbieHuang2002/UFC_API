from bs4 import BeautifulSoup
import lxml
import requests
import json
import re
import sys
from fighter import FighterStatsExtractor

class UpcomingFights:
    def __init__(self):
        pass

    def get_fights(self):
        url = 'https://www.ufc.com/events'
        page = requests.get(url)
        content = page.text
        soup = BeautifulSoup    


if __name__ == '__main__':
    print(UpcomingFights().get_fights())