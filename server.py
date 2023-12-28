from flask import Flask
import webscraper
app = Flask(__name__)

@app.route('/return_fighter_stats/<firstname>/<lastname>', methods=['GET'])
def return_fighter_stats(firstname, lastname):
    return  webscraper.get_fighter_stats(firstname, lastname)

if __name__ == '__main__':
    app.run(debug=True)