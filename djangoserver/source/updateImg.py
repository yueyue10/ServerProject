import json
import sqlite3


# 更新图片路径工具类
class MySqlite(object):

    def __init__(self):
        self.conn = sqlite3.connect('../db.sqlite3')
        print('open database successfully')

    def insert_data(self):
        sql1_result = self.conn.execute("select * from miniprogram_gradetype")
        grade_types = sql1_result.fetchall()
        self.conn.commit()
        for gradeT in grade_types:
            gradeItem = list(gradeT)
            # print(gradeItem)
            grade_id = gradeItem[0]
            grade_image = gradeItem[2]
            grade_image = grade_image.replace('http://pics.shicimingju.com/', 'http://www.shicimingju.com/pics/')
            grade_image = grade_image.replace(' ', '')
            sql1 = "update miniprogram_gradetype set grade_image ='%s' where id = %d;" % (grade_image, grade_id)
            self.conn.execute(sql1)
            self.conn.commit()
            print(sql1)
        self.conn.close()


if __name__ == '__main__':
    mySql = MySqlite()
    mySql.insert_data()
