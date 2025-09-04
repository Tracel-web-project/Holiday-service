from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)  # allow frontend requests

# Connect to MongoDB (same URI you used)
client = MongoClient("mongodb://holidays-mongo:27017/")  
#client = MongoClient("mongodb://localhost:27017/")  # ⚡ change if using Docker
db = client["holidaysdb"]
holidays_collection = db["holidays"]
client = MongoClient("mongodb://holidays-mongo:27017/")  # use container name


# GET all holidays
@app.route("/holidays", methods=["GET"])
def get_holidays():
    holidays = list(holidays_collection.find({}, {"_id": 0}))
    return jsonify(holidays)

# POST new holiday
@app.route("/holidays", methods=["POST"])
def create_holiday():
    holiday_data = request.json
    holidays_collection.insert_one(holiday_data)
    holiday_data.pop("_id", None)  # remove ObjectId if exists
    return jsonify(holiday_data), 201

@app.route("/book", methods=["POST"])
def book_holiday():
    data = request.json  # { holiday, user, days }
    holidays_collection.insert_one(data)  # saves booking
    return jsonify({"message": "Holiday booked successfully", "holiday": data["holiday"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
