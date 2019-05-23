# coding=UTF8
import datetime
import sqlite3
import ipaddress

import pandas as pd
import requests
# import tqdm


# 遍歷 Dataframe，Insert or REPLACE 資料表
def UpdateDB():
    for index, row in inMonDF.iterrows():
        c.execute('INSERT INTO HistoryARP ("ADDRESS", "NAME", "MAC", "MANUFACTURER", "INTERFACE", "DATE") \
                   VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'.format(row['ADDRESS'], row['NAME'], row['MAC'], row['MANUFACTURER'], row['INTERFACE'], NowTime))


# 增加時間戳
def timestamp():
    ts = '[' + datetime.datetime.now().strftime("%m-%d %H:%M:%S") + '] '
    return ts


# 建立 sqlite database
conn = sqlite3.connect('Host_List.db')
c = conn.cursor()
print(timestamp(), '連線 Host_List.db 完成')


# InMon > Reports > Query > List Hosts > HTML
url = 'http://163.18.2.13/inmsf/Report?action=run&group=base&report=hostlist&type=table&instance=0&section=0&input_path=&authenticate=basic&resultFormat=html'

inMonReq = requests.get(url, auth=('logicalis', 'logicalis@kh'))
print(timestamp(), '取得 inMon_list_hosts_report.html')
inMonData = inMonReq.content

# pd.read_html 取回資料型態為由數個 Dataframe 組成的 List，因此加上 [0] 只取出第一個 Dataframe
inMonDF = pd.read_html(inMonData)[0]

# 重新命名 inMonDF 以符合 sqlite 欄位
inMonDF = inMonDF.rename(columns={"Name": "NAME",
                                  "Address": "ADDRESS",
                                  "MAC Address": "MAC",
                                  "MAC Manufacturer": "MANUFACTURER",
                                  "Interface": "INTERFACE"})
# 將 ADDRESS 欄為空的資料清除掉
inMonDF = inMonDF[inMonDF['ADDRESS'].notnull()]
inMonDF['DATE'] = datetime.datetime.now()
NowTime = datetime.datetime.now()
# 將 ADDRESS 轉換成 Interger
for index, row in inMonDF.iterrows():
    inMonDF.at[index, 'ADDRESS'] = int(ipaddress.IPv4Address(row['ADDRESS']))
try:
    # 建立 TABLE
    c.execute('CREATE TABLE "HistoryARP" ( "Name" TEXT, \
                            "ADDRESS" INTEGER NOT NULL, \
                            "MAC" TEXT, \
                            "MANUFACTURER" TEXT, \
                            "INTERFACE" TEXT, \
                            "DATE" TIMESTAMP )')
    print(timestamp(), '建立 "HistoryARP" Table')
    print(timestamp(), '資料庫更新開始')
    UpdateDB()
    print(timestamp(), '資料庫更新完畢')
    conn.commit()
    print(timestamp(), '保存資料庫更新')
    conn.close()
    print(timestamp(), '斷開資料庫連線')
except sqlite3.OperationalError:
    # 若 TABLE 已存在則直接進行更新
    print(timestamp(), '資料庫更新開始')
    UpdateDB()
    print(timestamp(), '資料庫更新完畢')
    conn.commit()
    print(timestamp(), '保存資料庫更新')
    conn.close()
    print(timestamp(), '斷開資料庫連線')
