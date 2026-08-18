from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from hospital_search import search_hospitals

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
db = SQLAlchemy(app)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500))
    distance_km = db.Column(db.Float)
    phone = db.Column(db.String(50))


with app.app_context():
    db.create_all()


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


@app.route("/bookmarks", methods=["GET"])
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    result = []
    for b in bookmarks:
        result.append({
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "distance_km": b.distance_km,
            "phone": b.phone
        })
    return jsonify(result)


@app.route("/bookmarks", methods=["POST"])
def add_bookmark():
    data = request.get_json()

    new_bookmark = Bookmark(
        name=data.get("name"),
        address=data.get("address"),
        distance_km=data.get("distance_km"),
        phone=data.get("phone")
    )
    db.session.add(new_bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark added", "id": new_bookmark.id})


@app.route("/bookmarks/<int:bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get(bookmark_id)
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({"message": "Deleted"})
    return jsonify({"message": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)