import json
from bs4 import BeautifulSoup
import requests
from fighter import FighterStatsExtractor
from top_fighters import UFCRankingScraper

class TextToJSON:
    def __init__(self, filname='data.json'):
        self.filename = filname
        self.data = {}

    def add_text(self, key, text):
        self.data[key] = text
    
    def upload_to_json(self):
        with open(self.filename, 'w') as json_file:
            json.dump(self.data, json_file, indent=1)

