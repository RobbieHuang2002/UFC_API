import json
from bs4 import BeautifulSoup
import requests
from fighter import FighterStatsExtractor
from top_fighters import UFCRankingScraper
from upload_to_json import TextToJSON



if __name__ == '__main__':
    uploader = TextToJSON()
    names = UFCRankingScraper().get_top_fighters('Middleweight')
    get_fighter = FighterStatsExtractor()
    
    for name in names:
        full_name = name.split()
        if(len(full_name) == 3):
            first_name = full_name[0]
            middle_name = full_name[1]
            last_name = full_name[2]
            uploader.add_text(name, get_fighter.get_fighter_stats(first_name, middle_name, last_name))
            uploader.upload_to_json()
        else:
            first_name = full_name[0]
            middle_name = None
            last_name = full_name[1]
            uploader.add_text(name, get_fighter.get_fighter_stats(first_name, middle_name, last_name))
            uploader.upload_to_json()
