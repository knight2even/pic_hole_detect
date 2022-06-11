# !/usr/bin/env python
# -*- coding:utf-8 -*-
import sqlite3

import schedule
import time
import random

def autoincre_pic_link():
    res_link = ""
    type = random.randint(101,106)
    if type==101:
        res_link = "https://2a.zol-img.com.cn/product/61_940x705/508/cehgIA3pGJU9k.jpg"
    elif type==102:
        res_link = "https://img.3dmgame.com/uploads/allimg/170410/323_170410154252_3_lit.jpg"
    elif type==103:
        res_link = "http://i1.073img.com/160203/17598486_164146_1.jpg"
    elif type==104:
        res_link = "http://i1.073img.com/140630/6647734_102612_1.jpg"
    elif type==105:
        res_link = "https://img.tt98.com/d/file/96kaifa/20190613201211939/5d020854109d1.jpg"
    elif type==106:
        res_link = "http://n.sinaimg.cn/front/480/w640h640/20181225/2O4m-hqtwzec1701687.jpg"
    return res_link

def insert_data():
    conn = sqlite3.connect("identifier.sqlite")
    cur = conn.cursor()
    i = 0
    res_list = []
    f = open('213.txt', encoding='gbk')
    for line in f:
        i += 1
        if i < 36:
            continue
        print(line.strip().split(" "))
        list = line.strip().split(" ")
        print(list[6],list[7],list[13],list[14])
        str = list[13]+"."+list[14]
        # time.sleep(7)
        sql = '''
                insert into hole_info(
                pic_link,hole_num,direct_distance,distance,diameter,hole_type)
                values (?,?,?,?,?,?)'''
        print(sql)     #输出查询语句，用来测试
        print(autoincre_pic_link())
        params = (autoincre_pic_link(),int(list[11]),int(int(list[5])/1000),list[6],list[7],str)
        cur.execute(sql,params)
        conn.commit()

    cur.close
    conn.close()

def job():
    insert_data()
    print("I'm working...")

schedule.every(4).seconds.do(job)



if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)