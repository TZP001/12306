import sqlite3
from flask import Flask


class trainDB(object):
    def __init__(self, db_name="./train.db"):
        self.db_name = db_name
        self.key = "12306"
        self.table_name = "TRAIN_TK"
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.create()

    def create(self):
        """
        创建数据库
        :return:
        """
        if self.check_table():
            return
        self.cur.execute('''CREATE TABLE %s (NAME   CHAR(50)  PRIMARY KEY  UNIQUE  NOT NULL,
                            TK   CHAR(50));''' % self.table_name)
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

    def update(self, tk_val):
        """
        有则改之，无则加之。更新或插入tk值
        :param tk_val: tk
        :return:
        """
        cursor_all = self.cur.execute("SELECT * from %s" % self.table_name)
        unique_key = [row[0] for row in cursor_all if row]
        if self.key not in unique_key:
            self.cur.execute('''INSERT INTO %s (NAME,TK) VALUES ('%s','%s')''' % (self.table_name, self.key, tk_val))
        else:
            self.cur.execute('''UPDATE %s set TK = "%s"  where NAME = "%s"''' % (self.table_name, tk_val, self.key))
        self.conn.commit()

    def fetch_tk(self):
        cursor = self.cur.execute("select TK from %s where NAME = '%s'" % (self.table_name, self.key))
        train_tk = [column[0] for column in cursor]
        if len(train_tk) == 0:
            return ""
        else:
            return train_tk[0]

    def close(self):
        self.cur.close()
        self.conn.close()


app = Flask(__name__)


@app.route('/<name>')
def hello_name(name):
    scramble_ticket = trainDB()
    tk = scramble_ticket.fetch_tk()
    if name == "get_tk" or name == "favicon.ico":
        scramble_ticket.close()
        return tk
    else:
        if tk != name:
            scramble_ticket.update(name)
            scramble_ticket.close()
        return 'Hello %s!' % name


if __name__ == '__main__':
    app.run(debug=True)
