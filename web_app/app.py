import json
import datetime
import MySQLdb
from flask import Flask, render_template, request, jsonify

EPOCH = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - EPOCH).total_seconds() * 1000.0

app = Flask(__name__)
db = MySQLdb.connect("localhost", "pi", "", "hims_db") or die("Could not connect to database")
db.autocommit(True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weights", methods=["GET"])
def weights():
    rows_items = []
    rows_weights = []

    with db.cursor() as cur:
        cur.execute("SELECT * FROM items")
        rows_items = cur.fetchall()

        cur.execute("SELECT * FROM weights")
        rows_weights = cur.fetchall()

        cur.close()

    res = {}

    for row in rows_items:
        nuid, name, threshold, state = row

        res[nuid] = {
            "name": name,
            "state": state,
            "threshold": threshold,
            "weights": [],
            "rate": None
        }

    agg = {}
    mem = {}

    for row in rows_weights:
        nuid, weight, created_at, is_begin_point, delta = row

        if nuid not in res:
            continue

        res[nuid]["weights"].append({
            "timestamp": created_at.isoformat(sep=" "),
            "weight": weight
        })
        
        if nuid not in agg:
            agg[nuid] = {
                "sum": 0,
                "count": 0
            }

        if nuid not in mem:
            mem[nuid] = {
                "begin_weight": None,
                "end_weight": None,
                "duration": None
            }

        # Rate of change in weight
        if is_begin_point:
            # Calculate rate of weight decrease of previous section
            if mem[nuid]["begin_weight"] != None and mem[nuid]["end_weight"] != None and mem[nuid]["duration"] != None:
                agg[nuid]["sum"] += (mem[nuid]["begin_weight"] - mem[nuid]["end_weight"]) / mem[nuid]["duration"]
                agg[nuid]["count"] += 1

            # Define new high point
            mem[nuid] = {
                "begin_weight": weight,
                "end_weight": None,
                "duration": None
            }
        else:
            # Update new low point
            mem[nuid]["end_weight"] = weight
            mem[nuid]["duration"] = delta

    # Calculate rate of weight decrease of last section
    for nuid in mem:
        if mem[nuid]["begin_weight"] != None and mem[nuid]["end_weight"] != None and mem[nuid]["duration"] != None:
            agg[nuid]["sum"] += (mem[nuid]["begin_weight"] - mem[nuid]["end_weight"]) / mem[nuid]["duration"]
            agg[nuid]["count"] += 1

    # Calculate average of all sections
    for nuid in agg:
        if agg[nuid]["count"] > 0:
            res[nuid]["rate"] = agg[nuid]["sum"] / agg[nuid]["count"]

    return jsonify(res)

@app.route("/item/<nuid>", methods=["POST"])
def update(nuid):
    field = request.form["field"]
    value = request.form["value"]

    with db.cursor() as cur:
        cur.execute("UPDATE items SET %s = '%s' WHERE id = '%s'" % (field, value, nuid))

        cur.close()

    res = { "status": 200, "message": "Successfully updated item." }

    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
