# -*- coding: utf-8 -*-
import sys

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi


reload(sys)
sys.setdefaultencoding('utf-8')


class WechatSpiderPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    '''保存到数据库中对应的class
           1、在settings.py文件中配置
           2、在自己实现的爬虫类中yield item,会自动执行'''

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        # 读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            # cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        adbapi.ping = True
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    # SQL语句在这里
    def _conditional_insert(self, tx, item):
        sql = "insert into weibo_copy(comment_cont,comment_screen_name,comment_id,user_id,create_time) values(%s,%s,%s,%s,%s)"
        params = (item['comment_cont'], item['comment_screen_name'], item['comment_id'], item['user_id'], item['create_time'])

        #防止写入数据库报错 emoji表情问题
        tx.execute('SET NAMES utf8mb4')
        tx.execute("SET CHARACTER SET utf8mb4")
        tx.execute("SET character_set_connection=utf8mb4")
        tx.execute(sql, params)


    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue