import serial
import json
import datetime
import MySQLdb
from flask import Flask, render_template, request, jsonify

EPOCH = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - EPOCH).total_seconds() * 1000.0

app = Flask(__name__)
db = MySQLdb.connect("localhost", "pi", "", "hims_db") or die("Could not connect to database")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weights", methods=["GET"])
def weights():
    rows_items = []
    rows_weights = []

    with db:
        cursor = db.cursor()

        cursor.execute("SELECT * FROM items")
        rows_items = cursor.fetchall()

        cursor.execute("SELECT * FROM weights")
        rows_weights = cursor.fetchall()

        cursor.close()

    res = {}

    for row in rows_items:
        nuid, name, threshold, state = row

        res[nuid] = {
            "name": name,
            "state": state,
            "threshold": threshold,
            "weights": []
        }

    for row in rows_weights:
        nuid, weight, created_at = row

        if nuid not in res:
            continue

        res[nuid]["weights"].append({
            "timestamp": created_at.isoformat(sep=" "),
            "weight": weight
        })

    #print(res)

    return jsonify(res)

@app.route("/item/<nuid>", methods=["POST"])
def update(nuid):
    field = request.form["field"]
    value = request.form["value"]

    with db:
        cursor = db.cursor()

        cursor.execute("UPDATE items SET %s = '%s' WHERE id = '%s'" % (field, value, nuid))

        cursor.close()

    res = { "status": 200, "message": "Successfully updated item." }

    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
