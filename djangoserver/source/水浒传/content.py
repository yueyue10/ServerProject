import json
import sqlite3


# 插入诗词内容工具类
class MySqlite(object):

    def __init__(self):
        self.conn = sqlite3.connect('../../db.sqlite3')
        print('open database successfully')

    def insert_data(self):
        with open('chapter.json', 'r', encoding='utf-8') as chapterStr:
            chapter = json.load(chapterStr)
            sql1 = 'insert into miniprogram_book(bookName, image, author, year, desc, chapters) values("%s","%s","%s","%s","%s","%s")' % (
                chapter['bookName'], chapter['image'], chapter['author'], chapter['year'], chapter['desc'],
                chapter['chapters'])
            self.conn.execute(sql1)
            self.conn.commit()
            # print(sql1)
        with open('content.json', 'r', encoding='utf-8') as contentStr:
            content = json.load(contentStr)
            for chapterObj in content['chapters']:
                paragraphs = json.dumps(chapterObj['paragraphs'])
                print(type(paragraphs), paragraphs)
                sql2 = 'insert into miniprogram_bookchapter(bookName, title, paragraphs) values("%s","%s","%s")' % (
                    content['name'], chapterObj['title'], '')
                self.conn.execute(sql2)
                self.conn.commit()
                print(sql2)
                sql3 = "update miniprogram_bookchapter set paragraphs ='%s' where title == '%s';" % (
                    paragraphs, chapterObj['title'])
                self.conn.execute(sql3)
                self.conn.commit()
                print(sql3)
        self.conn.close()


if __name__ == '__main__':
    mySql = MySqlite()
    mySql.insert_data()
