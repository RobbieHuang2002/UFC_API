from bs4 import BeautifulSoup
import lxml
import requests
import json


def get_fighter_stats(fighterFirstName, fighterLastName):
    url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterLastName}'
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, 'lxml')
    stats = soup.find_all('div', class_="athlete-stats__stat")
    stats_list = []
    for i in stats:
        stats_list.append(i.get_text())
    print(stats_list)

    fighter_stats = {
        'knockouts': stats_list[0].replace("\n", " "),
        'submissions':stats_list[1].replace("\n", " "),
        'firstRoundKnockouts': stats_list[2].replace("\n", " ")
    }

    print(fighter_stats)




get_fighter_stats('sean', 'strickland')

