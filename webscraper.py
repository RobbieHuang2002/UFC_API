from bs4 import BeautifulSoup
import lxml
import requests
import json
import re

def calculate_striking_accruacy(strikes):
    if strikes[0].get_text() == "":
        return 0
    if strikes[1].get_text() == "":
        return 0 
    else:
        accuracy = (int(strikes[0].get_text())/int(strikes[1].get_text()))
        return accuracy

def calculate_takedown_accuracy(strikes):
    if strikes[2].get_text() == "":
        return 0
    if strikes[3].get_text() == "":
        return 0
    else:
        accuracy = (int(strikes[2].get_text())/int(strikes[3].get_text()))
        return accuracy

def extract_records(input):
   matches = re.match(r'(\d+)-(\d+)-(\d+)', input)
   if matches:
        wins, losses, draws = map(int, matches.groups())
        return {'wins': wins, 'losses': losses, 'draws': draws}
   else:
       return None

def remove_unwanted_spaces(sentence):
    cleaned_sentence = re.sub(r'\s', ' ', sentence)
    cleaned_sentence = cleaned_sentence.strip()
    return cleaned_sentence

def get_fighter_stats(fighterFirstName, fighterLastName):
    url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterLastName}'
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, 'lxml')
    name = soup.find('h1', class_="hero-profile__name")
    age = soup.find('div', class_="field field--name-age field--type-integer field--label-hidden field__item")
    physique = soup.find_all('div', class_="c-bio__text")
    winning_stats = soup.find_all('div', class_="athlete-stats__stat")
    division = soup.find('p', class_="hero-profile__division-title").get_text()
    strikes = soup.find_all('dd', class_="c-overlap__stats-value")
    print(strikes)
    significant_strikes = soup.find_all('div', class_="c-stat-compare__number")
    record = soup.find('p', class_="hero-profile__division-body").get_text()
    fighter_stats = {
        'name': name.get_text(),
        'age': age.get_text(), 
        'divsion': division,
        'physique': {
            'height': None,
            'weight': None,
            'reach': None,
            'leg reach': None
        },
        'record': extract_records(record),
        'knockouts': None,
        'submissions': None,
        'FRF': None,
        'Stikes': {
            'landed': strikes[0].get_text(),
            'attempted': strikes[1].get_text(),
            'accuracy': calculate_striking_accruacy(strikes)
        },
        'offense': {
            'sig. str. landed. per min':remove_unwanted_spaces(significant_strikes[0].get_text()),
            'sig. str. absorbed. per min': remove_unwanted_spaces(significant_strikes[1].get_text()),
            'takedown avg': remove_unwanted_spaces(significant_strikes[2].get_text()),
            'submission avg':remove_unwanted_spaces(significant_strikes[3].get_text()),
        },
        'Takedowns': {
            'landed': strikes[2].get_text(),
            'attempted': strikes[3].get_text(),
            'accuracy': calculate_takedown_accuracy(strikes)
        }
    }
    
    for i in winning_stats:
        if "Knockout" in i.get_text():
            fighter_stats['knockouts'] = remove_unwanted_spaces(i.get_text())
        elif "Finishes" in i.get_text():
            fighter_stats['FRF'] = remove_unwanted_spaces(i.get_text())
        elif "Submission" in i.get_text():
            fighter_stats['submissions']  = remove_unwanted_spaces(i.get_text())

    print(fighter_stats)
     
get_fighter_stats('alex', 'pereira')

