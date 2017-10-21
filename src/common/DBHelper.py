# coding: utf-8
import pymysql
import traceback
import src.common.loadconf as config


class DBHelper:

    def __init__(self):
        self.conf = config.ConfigLoader('../../resources/db.properties')
        self.con = con = pymysql.connect(self.conf.get('db.host'), self.conf.get('db.username'), self.conf.get('db.pwd'),self.conf.get('db.dbname'))
        self.cursor = self.con.cursor()

    def query(self, sqlStr):
        if sqlStr is None or sqlStr == '':
            raise Exception("Invalid Sql Statemate!", 1)
        try:
            self.cursor.execute(sqlStr)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            print(traceback.print_exc())
            return ()

    def update(self, sqlStr):
        if sqlStr is None or sqlStr == '':
            raise Exception("Invalid Sql Statemate!", 1)
        try:
            self.cursor.execute(sqlStr)
            self.con.commit()
            return True
        except:
            self.con.rollback()
            print("Error: unable to fecth dataError: unable to fecth data")
            return  False

    def check_login(self, username, pwd):
        strSql = "select user_name,user_password from tb_users where user_name='NAME_PARAM' and user_password='PWD_PARAM'"
        strSql = strSql.replace('NAME_PARAM',username)
        strSql =strSql.replace('PWD_PARAM',pwd)
        return self.query(strSql)

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.con is not None:
            self.con.close()


def test():
    helper = DBHelper()
    print(helper.checkLogin("Tom","123456"))
    #print helper.query("select user_name,user_password from users where user_name='Tom' and user_password='123456'")
    helper.close()
