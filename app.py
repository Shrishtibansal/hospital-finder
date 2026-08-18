from flask import Flask, render_template, request, jsonify
from hospital_search import search_hospitals

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find-hospitals", methods=["POST"])
def find_hospitals():
    data = request.get_json()
    user_lat = data.get("latitude")
    user_lon = data.get("longitude")
    city = data.get("city", "")
    specialty = data.get("specialty", "")

    results = search_hospitals(city, user_lat, user_lon, specialty)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)