from bs4 import BeautifulSoup
import requests

# url = 'https://www.ufc.com'

# page = requests.get(url)

# soup = BeautifulSoup(page.text, features='html.parser')


def search_fighter(fighterFirstName, fighterLastName):
    url = f'https://www.ufc.com/athlete/{fighterFirstName}-{fighterLastName}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    soup.find_all('p')
    print(soup)
search_fighter('sean', 'strickland')

