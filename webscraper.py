from bs4 import BeautifulSoup
import lxml
import requests
import json


def get_fighter_stats(fighterFirstName, fighterLastName):
    url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterLastName}'
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, 'lxml')
    winning_stats = soup.find_all('div', class_="athlete-stats__stat")
    wins = soup.find_all('div', class_="hero-profile__division")
    division = soup.find('p', class_="hero-profile__division-title").get_text()
    strikes = soup.find_all('dd', class_="c-overlap__stats-value")
    record = soup.find('p', class_="hero-profile__division-body").get_text()
    stats_list = []
    fighter_stats = {
        'name': None,
        'age': None, 
        'divsion': division,
        'record': record,
        'knockouts': None,
        'submissions': None,
        'FRF': None,
        'Stikes': {
            'landed': strikes[0].get_text(),
            'attempted': strikes[1].get_text(),
            'accuracy': (int(strikes[0].get_text())/int(strikes[1].get_text()))
        },
        'Takedowns': {
            'landed': strikes[2].get_text(),
            'attempted': strikes[3].get_text(),
            'accuracy': (int(strikes[2].get_text())/int(strikes[3].get_text()))
        }
    }
    
    for i in winning_stats:
        if "Knockout" in i.get_text().replace("\n", " "):
            fighter_stats['knockouts'] = i.get_text().replace("\n", " ")
        elif "Finishes" in i.get_text().replace("\n", " "):
            fighter_stats['FRF'] = i.get_text().replace("\n", " ")
        elif "Submission" in i.get_text().replace("\n", " "):
            fighter_stats['submissions']  = i.get_text().replace("\n", " ")
        # stats_list.append(i.get_text())

    print(fighter_stats)
     
get_fighter_stats('sean', 'strickland')

