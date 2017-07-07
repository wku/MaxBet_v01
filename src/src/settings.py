# coding=utf-8


import datetime
import time
import json



#######################################


#server
SERVER = True

#home
SERVER = False

#in INFO
# LOGER = True

#in CRITICAL
LOGER = False




base_url = 'http://www.maxbet.com/Default.aspx'

PORTS ={
    "1": 52000,
    "2": 52001,
    "3": 52002,
    "4": 52003,
    "5": 52004,
}


Userlogin = {
    "1": "KKFBLKB52P",
    "2": "KKFBLKB53P",

    "3": "KKFBLKB54P",

    "4": "KKFBLKB55P",
    "5": "KKFBLKB51P"
}

UserPassword = {
    "1": "Aa200200",
    "2": "Aa200200",

    "3": "Aa200200",

    "4": "Aa200200",
    "5": "q123654"
}

login_UserName_loc = "txtID"
login_Password_loc = "txtPW"
login_SignIn_loc = "largeBtn"


#######################################
#
#
# import sys
#
# print(time.time())
#
# #
#
#
#
# # tstamp  = 1485875900084/1000
# # globalshowtime = 1485873000
# # kickofftime = 1485872940
# # livetimer = 1485873122
# # real = 1485875305
# # 2017-01-31 17:18:20.084000
# # 2017-01-31 16:30:00
# # 2017-01-31 16:29:00
# # 2017-01-31 16:32:02
# # 2017-01-31 17:08:25
# #
# tstamp  = 1485876370885/1000
# globalshowtime = 1485873000
# kickofftime = 1485872940
# livetimer = 1485876369
# real = 1485876535
# # 2017-01-31 17:26:10.885000
#     # 2017-01-31 16:30:00
#     # 2017-01-31 16:29:00
# # 2017-01-31 17:26:09
# # 2017-01-31 17:28:55
#
#
#
# print(datetime.datetime.fromtimestamp(tstamp))
# print(datetime.datetime.fromtimestamp(globalshowtime))
# print(datetime.datetime.fromtimestamp(kickofftime))
# print(datetime.datetime.fromtimestamp(livetimer))
# print(datetime.datetime.fromtimestamp(real))
#
# diff = (datetime.datetime.fromtimestamp(real) - datetime.datetime.fromtimestamp(livetimer))
# kf = 0
# date = str(int((diff.total_seconds() % 3600) // 60) + kf)
# print (date)
#
# live =False
# diff = (datetime.datetime.fromtimestamp(kickofftime ) - datetime.datetime.fromtimestamp(globalshowtime))
# print ('live: ', diff.total_seconds())
# if diff.total_seconds()<0:
#     add = True
#
# print (add)
#
#
#
#
# sys.exit()
# print ("###############")
#
#
#
#
#
#
#
#
#
# tstamp  = 1485871237465/1000
# globalshowtime = 1485871200
# kickofftime = 1485871140
# livetimer = 1485871140
#
# real = 1485871271 #
#
# # print(time.time())
# # time.sleep(1)
# # print(time.time())
#
# print(datetime.datetime.fromtimestamp(tstamp))
# print(datetime.datetime.fromtimestamp(globalshowtime))
# print(datetime.datetime.fromtimestamp(kickofftime))
# print(datetime.datetime.fromtimestamp(livetimer))
# print(datetime.datetime.fromtimestamp(real))
#
# add = ''
# diff = (datetime.datetime.fromtimestamp(tstamp ) - datetime.datetime.fromtimestamp(real))
# print (diff.total_seconds())
# if diff.total_seconds()<0: add = add+ "."
# diff = (datetime.datetime.fromtimestamp(livetimer) - datetime.datetime.fromtimestamp(globalshowtime))
# print (diff.total_seconds())
# if diff.total_seconds()<0: add = add+ ","
# print (add)
# sys.exit()
#
#
#
#
#
