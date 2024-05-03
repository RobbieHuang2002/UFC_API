from flask import Flask, request, jsonify
from fighter import FighterStatsExtractor

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    if request.method=='GET':
        return "Home"

@app.route("/fighter", methods=['GET'])
def fighter():
    if request.method=='GET':
        firstName = request.args.get('firstName')
        middleName = request.args.get('middleName')
        lastName = request.args.get('lastName')
        stats = FighterStatsExtractor().get_fighter_stats(firstName, middleName, lastName)
        return jsonify(stats), 200


if __name__ == '__main__':
    app.run(debug=True)
