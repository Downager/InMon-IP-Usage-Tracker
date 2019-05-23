# coding=UTF8
import sqlite3
from flask import Flask, g, render_template, request
import ipaddress


app = Flask(__name__)
SQLITE_DB_PATH = 'Host_List.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
    return db


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # Get the database connection
    db = get_db()
    # Form 資料處理
    address = request.form['address']
    netmask = request.form['netmask']
    daterange = request.form['daterange']
    record = request.form['record']
    cidr = address + netmask

    # 將發來的 CIDR 轉成 interger (配合 DB 內 IP 存放型態)
    interface = ipaddress.IPv4Interface(cidr)
    startip = int(interface.network.network_address)
    endip = int(interface.network.broadcast_address)
    ip = int(interface.ip)
    SQLCMD_DATE = ''
    SQLCMD_GROUP = ' group by `ADDRESS`'
    SQLCMD_ORDER = ' order by `ADDRESS`'
    SQLCMD_LIMIT = ' limit 2160'
    # 新增日期篩選
    if daterange != 'all':
        SQLCMD_DATE = " AND `DATE` < date('now', '-{} day')".format(int(daterange))
    # Host 搜尋
    if netmask == '/32':
        SQLCMD_SEARCH = 'SELECT * FROM `HistoryARP` WHERE `ADDRESS` = "{}"'.format(ip)
    # Netmask 搜尋
    else:
        SQLCMD_SEARCH = 'SELECT * FROM `HistoryARP` WHERE `ADDRESS` BETWEEN {} AND {}'.format(startip, endip)

    # 加上 group by `ADDRESS` 只取出最新一筆
    if record == 'latest':
        cursor = db.execute(SQLCMD_SEARCH + SQLCMD_DATE + SQLCMD_GROUP + SQLCMD_ORDER)
    # 不加上 group by 取出所有歷史資料 / 加上 limit 避免資料爆量 (24小時*30天*3個月=2160)
    elif record == 'history':
        cursor = db.execute(SQLCMD_SEARCH + SQLCMD_DATE + SQLCMD_ORDER + SQLCMD_LIMIT)

    rows = cursor.fetchall()

    if not rows:
        return '<h3>查無此筆資料</h3> \n <a href = "/">回到上一頁</a>'
    else:
        # 將 rows (tuple) 迭代成 result (list)
        result = [list(row) for row in rows]
        # 將 IP 資訊從 interger 轉回 IP addr.
        for row in result:
            row[1] = ipaddress.IPv4Address(row[1])
        return render_template("list.html", rows=result)


if __name__ == "__main__":
    app.run(debug=True)
