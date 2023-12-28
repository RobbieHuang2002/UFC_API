"""
Simple Terminal Application to interface with API, not meant to be used, just an example.
"""

import requests
import json
print("Welcome to the UFC Fighter Stats API")

while True:
    
    stdin = input("Full Name (space seperated): ")
    first = stdin.split()[0]
    last = stdin.split()[1]

    response = requests.get(f'http://127.0.0.1:5000/return_fighter_stats/{first}/{last}')
    print(response.content.decode('utf-8'))