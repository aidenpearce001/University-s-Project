from flask import Flask, render_template, request,jsonify
import requests
import json
import pymysql

app = Flask(__name__)

db = pymysql.connect( host = '127.0.0.1',
      user = 'root',passwd = '1234',database="restaurant")
cursor = db.cursor()

cursor.execute("DESCRIBE restaurant")
all_table = [x for x in cursor]

tables = [x[0] for x in all_table]
tables

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")
    # if request.method == 'POST':
    #     result = request.form
    #     data = result['search']

    #     sql = '%'+data+'%'
    #     cursor.execute("select * from restaurant where `Phục vụ các món` LIKE '%Thịt Gà%'")
    #     ls = [x for x in cursor]
    #     # return render_template("index.html",data=data)
    #     data = dict(zip(tables, ls[:10]))
    #     render_template("index.html",data=data)
    # else:
    #     return render_template("index.html")

@app.route("/top10", methods=["GET", "POST"])
def handle_request():
    if request.method == 'POST':
        result = request.form
        data = result['search']
        print(result['yes_no'])
        sql = '%'+data+'%'
        cursor.execute("select * from restaurant where `Phục vụ các món` LIKE '%Thịt Gà%'")
        ls = [x for x in cursor]
        # return render_template("index.html",data=data)
        data = dict(zip(tables, ls[0]))
        print(data)

        thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
        }
        # for key, value in data.items():

        # return data
        return render_template("result.html",data=data)
if __name__ == "__main__":
    app.run(debug=True)