# !/usr/bin/python
# -*- encoding: utf-8 -*-
from flask import Flask, render_template, request,jsonify
import requests
import json
import pymysql
import time

app = Flask(__name__)

db = pymysql.connect( host = '127.0.0.1',
      user = 'root',passwd = 'abc123@#$',database="restaurant")
cursor = db.cursor()

cursor.execute("DESCRIBE restaurant")
all_table = [x for x in cursor]

tables = [x[0] for x in all_table]

images_map = {}

explain = ["id","select_type","table","type","possible_keys","key","key_len","ref","filtered","rows","Time","Extra"]
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
        if request.args.get('loc'):
            loc = request.args.get('loc')
            print(loc)
            loc_sql = " And ( `địa điểm` like '%{}%')".format(loc)
        else:
            loc_sql = ""

        if request.args.get('style'):
            style = request.args.get('style')
            print(style)
            style_sql = " And ( `Phong cách ẩm thực` like '%{}%')".format(style)
        else:
            style_sql = ""
        sql = "SELECT * FROM restaurant INNER JOIN rating ON restaurant.ID = rating.restaurant_id where "
        sql_order = "SELECT * FROM restaurant INNER JOIN rating ON restaurant.ID = rating.restaurant_id WHERE ( `Phục vụ các món` like '%Cơm%') And ( `Phong cách ẩm thực` like '%Hàn%') ORDER BY avg"
        for i in data.split(","):
            sql += "( `Phục vụ các món` like " + "'%" +i + "%') AND " 
        sql = sql[:-5] + loc_sql + style_sql + " ORDER BY avg DESC"
        print(sql)
        # cursor.execute("SELECT restaurant_id FROM rating")
        # print([x for x in cursor])
        cursor.execute(sql)
        ls = [x for x in cursor]
        # return render_template("index.html",data=data)
        dict1 = dict(zip(tables, ls[:10]))
        data = {}
        for i,v in enumerate([v[1] for k,v in dict1.items()]):
            data[v] = dict(zip(tables, ls[i]))

        cursor.execute("EXPLAIN "+sql)
        perform = cursor.fetchall()
        for i in perform:
            for _,k in enumerate(i):
                print(explain[_]+" : "+str(k))
        # return data
        if len(data) == 0:
            return render_template("nothing.html")
        else:
            return render_template("row-listings-filterstop-search-aside.html",data=data,images_map=images_map)
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
