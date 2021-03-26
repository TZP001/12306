import sqlite3
from flask import Flask


class trainDB(object):
    def __init__(self, db_name="./train.db"):
        self.db_name = db_name
        self.key = "12306"
        self.table_name = "TRAIN_TK"
        self.conn = sqlite3.connect(self.db_name, timeout=3, isolation_level=None, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create()

    def create(self, is_force=False):
        """
        创建数据库
        :param is_force: 是否强制创建表（先删除再创建）
        :return: 
        """
        if is_force:
            self.cur.execute('''DROP TABLE %s;''' % self.table_name)
        if self.check_table():
            return
        self.cur.execute('''CREATE TABLE %s (NAME   CHAR(50)  PRIMARY KEY  UNIQUE  NOT NULL,
                            TK   CHAR(50),
                            RAIL_DEVICEID CHAR(300),
                            RAIL_EXPIRATION CHAR(50));''' % self.table_name)
        self.conn.commit()

    def check_table(self):
        """
        检查数据库是否存在表 self.table_name
        :return: True/False
        """
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tab_names = [row[0] for row in self.cur.fetchall() if row]
        if self.table_name in tab_names:
            return True
        else:
            return False

    def update(self, name, tr_val):
        """
        有则改之，无则加之。更新或插入tk值
        :param name: tk/RAIL_EXPIRATION/RAIL_DEVICEID 其中一种
        :param tr_val: 它们的值
        :return:
        """
        cursor_all = self.cur.execute("SELECT * from %s" % self.table_name)
        unique_key = [row[0] for row in cursor_all if row]
        if self.key not in unique_key:
            self.cur.execute(
                '''INSERT INTO %s (NAME,%s) VALUES ('%s','%s')''' % (self.table_name, name, self.key, tr_val))
        else:
            self.cur.execute(
                '''UPDATE %s set %s = "%s"  where NAME = "%s"''' % (self.table_name, name, tr_val, self.key))
        self.conn.commit()

    def fetch_by_name(self, name):
        """
        查询数据
        :param name: 记录名
        :return: 值
        """
        cursor = self.cur.execute("select %s from %s where NAME = '%s'" % (name, self.table_name, self.key))
        train_tk = [column[0] for column in cursor]
        if len(train_tk) == 0:
            return ""
        else:
            return train_tk[0]

    def close(self):
        self.cur.close()
        self.conn.close()


app = Flask(__name__)

ticket = trainDB()
tk = ticket.fetch_by_name("TK")
rd = ticket.fetch_by_name("RAIL_DEVICEID")
re = ticket.fetch_by_name("RAIL_EXPIRATION")


@app.route('/')
def hello_world():
    return '欢迎来到flask 12306抢票界面'


@app.route('/set_tk/<name>')
def set_tk(name):
    if tk != name:
        ticket.update("TK", name)
        return "TK 更新成功"
    else:
        return "无需更新"


@app.route('/set_rd/<name>')
def set_rd(name):
    if rd != name:
        ticket.update("RAIL_DEVICEID", name)
        return "RAIL_DEVICEID 更新成功"
    else:
        return "无需更新"


@app.route('/set_re/<name>')
def set_re(name):
    if re != name:
        ticket.update("RAIL_EXPIRATION", name)
        return "RAIL_EXPIRATION更新成功"
    else:
        return "无需更新"


@app.route('/get_tk')
def get_tk():
    return tk


@app.route('/get_rd')
def get_rd():
    return rd


@app.route('/get_re')
def get_re():
    return re


if __name__ == '__main__':
    app.run(debug=True)
