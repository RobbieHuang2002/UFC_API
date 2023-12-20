from bs4 import BeautifulSoup
import requests

url = 'https://www.ufc.com'

page = requests.get(url)

soup = BeautifulSoup(page.text, features='html.parser')

print(soup)

