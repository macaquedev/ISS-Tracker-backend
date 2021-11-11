from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import datetime

app = Flask(__name__)
CORS(app)
epoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds()


@app.route('/', methods=['POST'])
def home():
    content = request.json
    base_date = datetime.datetime(content["year"], content["month"] + 1, content["day"],
                                  content["hour"], content["minute"], 0)
    timestamp1 = unix_time_millis(base_date + datetime.timedelta(hours=1))
    timestamp2 = unix_time_millis(base_date + datetime.timedelta(hours=-1))
    iss_response = requests.get(
        f"https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps="
        f"{timestamp1},{timestamp2}").json()
    return jsonify(iss_response)


if __name__ == '__main__':
    app.run(debug=True)