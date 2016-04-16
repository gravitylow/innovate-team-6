from flask import Flask
import MySQLdb
import json

app = Flask(__name__)
app.config['DEBUG'] = True

db = MySQLdb.connect(host="ec2-54-152-223-36.compute-1.amazonaws.com",
                     user="root",
                     passwd="alpine",
                     db="IRS_DB")

cursor = db.cursor()

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/incidentsubtype/<int:itype>")
def incident_subtype(itype):
    cursor.execute("SELECT * FROM INCIDENT_SUBTYPE WHERE IST_TYPEID = '" + itype + "'")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/incidenttype")
def incident_type():
    cursor.execute("SELECT * FROM INCIDENT_TYPE")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/severities")
def severities():
    cursor.execute("SELECT * FROM SEVERITies")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);


@app.route("/severities/<int:sev_id>", methods=['GET'])
def severitiesByID(sev_id):
    cursor.execute("SELECT * FROM SEVERITies WHERE SEV_ID = " + str(sev_id))
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);


if __name__ == "__main__":
    app.run()
