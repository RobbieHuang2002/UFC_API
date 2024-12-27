from bs4 import BeautifulSoup
import lxml
import requests
import json
import re
import sys

class ActiveFighterNameExtractor:
    def __init__(self):
        pass


    def split_name(self, name):
        cleaned_name = " ".join(name.split())

        parts = cleaned_name.split()

        if len(parts) == 1:
            return parts[0], "", ""
        elif len(parts) == 2:
            return parts[0], "", parts[1]
        else:
            return parts[0], " ".join(parts[1:-1]), parts[-1]
            
    def extractName(self):
        counter = 1
        result = []
        previous_data = None
        while True:
            print(f"Fetching page {counter}...")
            url = 'https://www.ufc.com/athletes/all'
            response = requests.get(url, params={"page": counter, "filters[0]": "status:23"})
            
            soup = BeautifulSoup(response.text, "html.parser")

            fighters = soup.find_all("div", class_="c-listing-athlete-flipcard white")
            if fighters == previous_data:
                print("no more new data")
                break

            for fighter in fighters:
                fighter_name = fighter.find('span', class_="c-listing-athlete__name")
                firstname, middlename, lastname = ActiveFighterNameExtractor().split_name(fighter_name.get_text())
                result.append([firstname, middlename, lastname])
                

            counter += 1
            previous_data = fighters
        print(len(result))
        return(result)
if __name__ == '__main__':
    print(ActiveFighterNameExtractor().extractName())