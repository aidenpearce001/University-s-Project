from flask import Flask, render_template, request,jsonify
import requests
import json
import pymysql
import time

app = Flask(__name__)

db = pymysql.connect( host = '127.0.0.1',
      user = 'root',passwd = '1234',database="restaurant")
cursor = db.cursor()

cursor.execute("DESCRIBE restaurant")
all_table = [x for x in cursor]

tables = [x[0] for x in all_table]

images_map = {}
with open('images_map','r',encoding='utf-8') as fd:
    for i in fd:
        images_map[i.split(":")[0]] = i.split(":")[-1].rstrip()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index-template.html")
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
    # if request.method = "GET":
    #result = request.form
    #     pass
    if request.args:
        # language = request.args.get('food')
        # print(language)
        # return '''<h1>The language value is: {}</h1>'''.format(language)
        # result = request.form
        data = request.args.get('food')
        # print(result['loc'])
        # print(result['yes_no'])

        sql = "SELECT * FROM restaurant where "
        for i in data.split(","):
            sql += "( `Phục vụ các món` like " + "'%" +i + "%') AND " 

        # str1 = ''.join(sql.split("AND")[:-1])
        sql[:-5]
        # sql = '%'+data+'%'
        # cursor.execute("SELECT * FROM restaurant where ( `Phục vụ các món` like '%Thịt Gà%') AND (`Phục vụ các món` like '%Tôm%')")
        t1 = time.time()
        cursor.execute(sql[:-5])
        t2 = time.time()
        print('take : '+str(t2-t1)+'s')
        ls = [x for x in cursor]
        # return render_template("index.html",data=data)
        dict1 = dict(zip(tables, ls[:10]))
        data = {}
        for i,v in enumerate([v[1] for k,v in dict1.items()]):
            data[v] = dict(zip(tables, ls[i]))
        
        print(data)
        for k,v in data.items():
            # print(k)
            print(images_map[k])
        print(cursor.execute("EXPLAIN select * from restaurant where `Phục vụ các món` LIKE '%Thịt Gà%'"))
        # return data
        return render_template("row-listings-filterstop-search-aside.html",data=data,images_map=images_map)
if __name__ == "__main__":
    app.run(debug=True)