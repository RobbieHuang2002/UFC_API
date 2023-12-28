# UFC API

This project provides an API for retrieving UFC fighter stats. It scrapes data from the official UFC website and serves it through a simple Flask server. You can query the API for a fighter's stats by providing their first and last name.

## Features

- Fetch fighter stats by name
- Data includes: name, age, division, physique, record, knockouts, submissions, strikes, offense, and takedowns
- Simple terminal client for testing the API

## Installation

1. Clone this repository:
```sh
git clone https://github.com/yourusername/UFC_API.git
```

2. Navigate to project directory
```sh
cd UFC_API
```

3. Install required packages
```sh
pip install -r requirements.txt
```

## Usage

1. Start the server
```sh
python3 server.py
```

2. Make a `GET` request, this is what the endpoint looks like:
```sh
<url>/return_fighter_stats/<firstname>/<lastname>
```
By default flask uses http://127.0.0.1:5000