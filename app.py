from flask import Flask, render_template, request, redirect
import pyttsx3
import sqlite3
import time
from threading import Timer
app = Flask(__name__)

seconds = 0

def alertpass():
    global seconds
    print("start to alert",seconds)
    engine = pyttsx3.init()
    if seconds > 0:
        engine.say("注意，注意，孔洞出现，孔洞出现")
    engine.runAndWait()
#查询孔洞数据
def select_data():
    conn = sqlite3.connect("identifier.sqlite")
    cur = conn.cursor()
    sql = "select * from hole_info where hole_num not in(103,104,107,108,112,116) and status = 0 order by direct_distance desc"
    cursor = cur.execute(sql)
    list = []
    for row in cursor:
        list.append(row)

    cur.close
    conn.close()
    return list

#查询上一个孔洞的位置
def select_last_distance():
    conn = sqlite3.connect("identifier.sqlite")
    cur = conn.cursor()
    sql = "select * from hole_info where hole_num not in(103,104,107,108,112,116) and status = 1 order by direct_distance limit 0,1"
    cursor = cur.execute(sql)
    list = []
    for row in cursor:
        list.append(row)

    cur.close
    conn.close()
    tmp = 0
    if len(list) > 0:
        tmp = list[0][4]
    return tmp

#把显示过的孔洞状态改变
def update_data(list):
    conn = sqlite3.connect("identifier.sqlite")
    cur = conn.cursor()
    for item in list:
        sql = "update hole_info set status=1 where id = " + str(item[0])
        print(item[0],type(item[0]))
        cur.execute(sql)
        conn.commit()
    cur.close
    conn.close()

#登录
@app.route('/', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'admin' and pwd == '123':  # 这里可以根据数据库里的用户和密码来判断，因为是最简单的登录界面，数据库学的不是很好，所有没用。
        return redirect('/index')
    else:
        return render_template('login.html', msg='用户名或密码输入错误')

@app.route('/index')
def hole_detect():  # put application's code here
    list = select_data()

    print(list)

    res_list = []
    if len(list) > 0:
        tmp = list[0][4]
        last_distance = select_last_distance()
        for item in list:
            if item[4] > tmp-1000:
                res_list.append(item)
        distance = last_distance - res_list[-1][4]

        global seconds

        if distance < 0:
            distance = 0
        else:
            if distance - 1000 > 0:
                seconds = ((distance - 1000) / 1000) * 60
                print("***" * 20)
                print(seconds, distance)

        #过掉的孔洞状态切换
        update_data(res_list)

        print(res_list)

        curtime = time.strftime('%H:%M:%S', time.localtime())

        if seconds > 0:
            # 指定seconds秒后执行alertpass警报函数
            t = Timer(seconds, alertpass)
            t.start()

        return render_template("index.html",last_distance=distance,list=res_list,curtime=curtime,seconds=seconds)
    else:
        return render_template("err.html",err="no more breaking paper")



if __name__ == '__main__':
    app.run()
