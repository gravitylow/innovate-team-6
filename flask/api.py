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

@app.route("/incident")
def incidents():
    cursor.execute("SELECT * FROM INCIDENTS")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/incident_submit", methods=['POST'])
def incidentSubmit():
    subtypeid = request.form['INC_SUBTYPEID']
    severityid = request.form['INC_SEVERITYID']
    contactname = request.form['INC_CONTACTNAME']
    contactphone = request.form['INC_CONTACTPHONE']
    description = request.form['INC_DESC']
    latitude = request.form['INC_LAT']
    longitude = request.form['INC_LONG']
    cursor.execute("""INSERT INTO INCIDENTS 
                   (INC_SUBTYPEID, INC_SEVERITYID, INC_CONTACTNAME, INC_CONTACTPHONE, INC_DESC, INC_LAT, INC_LONG)
                   VALUES (
                   """ + subtypeid + """,
                   """ + severityid + """,
                   """ + contactname + """,
                   """ + contactphone + """,
                   """ + description + """,
                   """ + latitude + """,
                   """ + longitude + ")")
    return 'OK, thanks luv you bye'

@app.route("/incident/<int:id>")
def incidentByID():
    cursor.execute("SELECT * FROM INCIDENTS WHERE INC_ID = " + str(id))
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/incidentsubtypes")
def incident_subtypes():
    cursor.execute("SELECT * FROM INCIDENT_SUBTYPE")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/incidentsubtype_by_id/<int:id>")
def incidentSubtypeByID(id):
    cursor.execute("SELECT * FROM INCIDENT_SUBTYPE WHERE IST_ID = " + str(id))
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/incidentsubtype_by_typeid/<int:itype>")
def incidentSubtypeByTypeID(itype):
    cursor.execute("SELECT * FROM INCIDENT_SUBTYPE WHERE IST_TYPEID = " + str(itype))
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/incidenttype")
def incidentType():
    cursor.execute("SELECT * FROM INCIDENT_TYPE")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/incidenttype/<int:id>")
def incidentTypeByID(id):
    cursor.execute("SELECT * FROM INCIDENT_TYPE WHERE INT_ID = " + str(id) + "'" )
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

#Severities
@app.route("/severities")
def severities():
    cursor.execute("SELECT * FROM SEVERITies")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);


@app.route("/severities/<int:sev_id>", methods=['GET'])
def severitiesByID(sev_id):
    cursor.execute("SELECT * FROM SEVERITies WHERE SEV_ID = " + str(sev_id) + "'")
    rows = cursor.fetchall()
    return json.dumps(rows, default=date_handler);

@app.route("/severities/<int:sev_id>", methods=['DELETE'])
def severitiesDeleteByID(sev_id):
    cursor.execute("DELETE FROM SEVERITies WHERE SEV_ID = " + str(sev_id))	
    return True;

if __name__ == "__main__":
    app.run()
