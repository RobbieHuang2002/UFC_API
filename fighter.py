from bs4 import BeautifulSoup
from datetime import datetime
import lxml
import requests
import json
import re
import sys
from top_fighters import UFCRankingScraper
import csv
import pandas as pd


class FighterStatsExtractor:
    def __init__(self):
        pass
    def find_available_bio_info(self, fighterFirstName, fighterMiddleName, fighterLastName):
        if fighterMiddleName is None or fighterMiddleName == '' or fighterMiddleName == '&':
            url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterLastName}'
        else:
            url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterMiddleName}-{fighterLastName}'
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        page = requests.get(url, headers=headers)
        content = page.text
        soup = BeautifulSoup(content, 'lxml')
        bio_title = [b.get_text() for b in soup.find_all('div', class_='c-bio__label')]
        bio_info = [b.get_text() for b in soup.find_all('div', class_="c-bio__text")]
        bio = {}
        for i in range(min(len(bio_title), len(bio_info))):
            bio[bio_title[i]] = bio_info[i]
        bio_cleaned = {k: v.strip() if isinstance(v, str) else v for k, v in bio.items()}

        return bio_cleaned



    def extract_physique(self, physique):
        cleaned_list = []
        for i in physique:
            cleaned_list.append(i.get_text())
        datalist = [cleaned_list[0]] + cleaned_list[-8:]
        variable_names = ['status', 'height', 'weight', 'debut', 'reach', 'leg reach']
        variables = {}
        for name, value in zip(variable_names, datalist + [None] * (len(variable_names)-len(datalist))):
            variables[name] = value
        
        return variables

    def calculate_striking_accruacy(self,strikes):
        if strikes[0].get_text() == "":
            return 0
        if strikes[1].get_text() == "":
            return 0 
        else:
            accuracy = int(int(strikes[0].get_text())/int(strikes[1].get_text()))
            return accuracy

    def calculate_takedown_accuracy(self, strikes):
        strikes_length = len(strikes)
        if strikes_length <=2:
            accuracy = 0
        else:
            if strikes[2].get_text() == "":
                return 0
            if strikes[3].get_text() == "":
                return 0
            else:
                accuracy = int(int(strikes[2].get_text())/int(strikes[3].get_text()))
                return accuracy

    def extract_records(self,input):
        matches = re.match(r'(\d+)-(\d+)-(\d+)', input)
        if matches:
                wins, losses, draws = map(int, matches.groups())
                return {'wins': wins, 'losses': losses, 'draws': draws}
        else:
            return {'wins': 0, 'losses': 0, 'draws': 0}

    def remove_unwanted_spaces(self,sentence):
        cleaned_sentence = re.sub(r'\s', ' ', sentence)
        cleaned_sentence = cleaned_sentence.strip()
        return cleaned_sentence

    def get_fighter_stats(self,fighterFirstName,fighterMiddleName,fighterLastName):
        if fighterMiddleName is None or fighterMiddleName == '' or fighterMiddleName == '&':
            url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterLastName}'
        else:
            url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterMiddleName}-{fighterLastName}'
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        page = requests.get(url, headers=headers)
        content = page.text
        soup = BeautifulSoup(content, 'lxml')
        name = soup.find('h1', class_="hero-profile__name") 
        if name:
            parts = name.get_text().strip().split()
        else:
            print("Name not found")
        # Split the name into first, middle, and last name
        first_name = middle_name = last_name = None
        if parts:
            if len(parts) == 1:
                first_name = parts[0]
            elif len(parts) == 2:
                first_name, last_name = parts
            elif len(parts) == 3:
                first_name, middle_name, last_name = parts
            else:
                # If more than 3 parts, assume first is first name, last is last name, middle is everything in between
                first_name = parts[0]
                last_name = parts[-1]
                middle_name = " ".join(parts[1:-1])
        age = soup.find('div', class_="field field--name-age field--type-integer field--label-hidden field__item")
        physique = soup.find_all('div', class_="c-bio__text")
        print(physique)
        winning_stats = soup.find_all('div', class_="athlete-stats__stat")
        division_elem = soup.find('p', class_="hero-profile__division-title")
        strikes = soup.find_all('dd', class_="c-overlap__stats-value")
        length_of_strikes = len(strikes)        
        significant_strikes = soup.find_all('div', class_="c-stat-compare__number")
        record_elem = soup.find('p', class_="hero-profile__division-body")
        # print(self.extract_physique(physique))
        fighter_stats = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'age': age.get_text() if age else None, 
            'divsion': division_elem.get_text() if division_elem else None,
            # 'physique': self.extract_physique(physique),
            # 'record': self.extract_records(record_elem.get_text() if record_elem else ''),
            'knockouts': None,
            'submissions': None,
            'FRF': None,
            'strikes_landed': strikes[0].get_text(),
            'strikes_attemped': strikes[1].get_text(),
            'strike_accuracy': self.calculate_striking_accruacy(strikes),
            'sig_str_landed_per_min': self.remove_unwanted_spaces(significant_strikes[0].get_text()),
            'sig_str_absorbed_per_min': self.remove_unwanted_spaces(significant_strikes[1].get_text()),
            'takedown_avg': self.remove_unwanted_spaces(significant_strikes[2].get_text()),
            'submission_avg': self.remove_unwanted_spaces(significant_strikes[3].get_text()),
            'takedown_landed': strikes[2].get_text() if length_of_strikes == 4 else None,
            'takedown_attempted': strikes[3].get_text() if length_of_strikes == 4 else None,
            'takedown_accuracy': self.calculate_takedown_accuracy(strikes)
        }
        bio = self.find_available_bio_info(fighterFirstName, fighterMiddleName, fighterLastName)
        fighter_stats.update(bio)
        
        record = self.extract_records(record_elem.get_text() if record_elem else '')
        fighter_stats.update(record)
        
        for i in winning_stats:
            text = i.get_text()
            if "Knockout" in text:
                numbers = re.findall(r'\d+', text)
                fighter_stats['knockouts'] = int(numbers[0]) if numbers else 0
            elif "Finishes" in text:
                numbers = re.findall(r'\d+', text)
                fighter_stats['FRF'] = int(numbers[0]) if numbers else 0
            elif "Submission" in text:
                numbers = re.findall(r'\d+', text)
                fighter_stats['submissions'] = int(numbers[0]) if numbers else 0

        return fighter_stats
    
    def add_to_csv(self, fighter_stats):
        df = pd.DataFrame([fighter_stats])
        df.to_csv('fighter_stats.csv', index=False)
        return df
    


if __name__ == '__main__':
    data = FighterStatsExtractor().get_fighter_stats('sean', '', 'strickland')
    FighterStatsExtractor().add_to_csv(data)
    print(FighterStatsExtractor().find_available_bio_info('sean', '', 'strickland'))

