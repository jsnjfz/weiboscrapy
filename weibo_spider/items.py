# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class WeiboComment(Item):
    comment_cont = Field()
    comment_screen_name = Field()
    comment_id = Field()
    user_id = Field()
    create_time = Field()


