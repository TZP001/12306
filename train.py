import sqlite3
class novelDB(object):
    def __init__(self, db_name="./novel.db"):
        self.db_name = db_name
        self.connect()
        
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        
    def query(self,query_key, table_info):
        query_sql = '''SELECT %s from %s where %s = "%s"''' % \
            (query_key, table_info['TABLE_NAME'], table_info['pr_key_name'],table_info['pr_key'])
        de_sql = '''DROP TABLE %s;''' % (table_info['TABLE_NAME'])

        try:
            cursor = self.cur.execute(query_sql)
        except Exception as e:
            try:
                self.cur.execute(table_info['tb_sql'])
            except Exception as es:
                self.cur.execute(de_sql)
                self.cur.execute(table_info['tb_sql'])
            cursor = self.cur.execute(query_sql)
        data_tupple_list = cursor.fetchall()

        data_list = [str(i[0]) for i in data_tupple_list if i[0] != '']
        data = "".join(data_list)
        return data

    # 添加或更新数据库    
    def create(self, table_info):
        
        if self.query(table_info['pr_key_name'],table_info):
            self.cur.execute(table_info['up_sql'])
        else:
            self.cur.execute(table_info['ins_sql'])
            
        self.conn.commit()    
      
    def fetch_all(self, table_info): #字典形式输出
        cursor = self.cur.execute("select * from %s" % table_info['TABLE_NAME'])
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data_list =[]
        for row in rows:
            data_list.append(dict(zip(columns, row)))
        return data_list
        
    def close(self):
        self.cur.close()
        self.conn.close()

class book_info(object):
    def __init__(self, TK_V, novel_name="12306"):
        self.TABLE_NAME = "TK"
        self.name = novel_name
        self.pr_key_name = "NAME"
        self.pr_key = self.name
        self.TK_=TK_V
        self.tb_sql = '''CREATE TABLE TK 
                   (NAME   CHAR(50)  PRIMARY KEY  UNIQUE  NOT NULL,
                   _TK   CHAR(50));'''
        self.ins_sql = '''INSERT INTO TK (NAME,_TK)
            VALUES ('%s','%s')
            ''' % (self.name,self.TK_)
        self.up_sql = '''UPDATE TK set _TK = "%s"  where NAME = "%s"''' \
                    % (self.TK_,self.name)

from flask import Flask
app = Flask(__name__)

@app.route('/<name>')
def hello_name(name):
    aa=novelDB()
    kk=aa.fetch_all({'TABLE_NAME':"TK"})
    tk=[id['_TK'] for id in kk if id['NAME']=="12306"]
    if name == "get_tk":
        return tk[0]
    else:
        if tk[0]!=name:
            novel_DB = novelDB()
            dd_bot=["1","2"]
            dd_bot[1]="12306"
            dd_bot[0]=name
            dd=book_info(dd_bot[0],dd_bot[1])
            novel_DB.create(dd.__dict__)
        else:
            pass
        return 'Hello %s!' % name

if __name__ == '__main__':
    
   app.run(debug = True)
