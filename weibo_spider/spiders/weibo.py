# -*- coding: utf-8 -*-
import json
import scrapy

from bs4 import BeautifulSoup
from scrapy.conf import settings

from weibo_spider.items import WeiboComment
from weibo_spider.spiders import parse_emoji


class WeiboSpider(scrapy.Spider):
    name = "weibo"

    #取setting中的COOKIES
    cookie = settings['COOKIES']

    def start_requests(self):
        url_base = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4250748880958571'
        yield scrapy.Request(url=url_base, callback=self.parse, cookies=self.cookie)

    def parse(self, response):
        print response.body

        cont = get_html_cont(response.body)

        soup = BeautifulSoup(cont, 'html5lib')
        comments = soup.find(attrs={'node-type': 'comment_list'}).find_all(attrs={'class': 'list_li S_line1 clearfix'})

        for comment in comments:
            wb_comment = WeiboComment()
            try:
                cont = []
                first_author = True
                first_colon = True
                for content in comment.find(attrs={'class': 'WB_text'}).contents:
                    if not content:
                        continue
                    if content.name == 'a':
                        if first_author:
                            first_author = False
                            continue
                        else:
                            if content.text:
                                cont.append(content.text)

                    elif content.name == 'img':
                        img_title = content.get('title', '')
                        if img_title == '':
                            img_title = content.get('alt', '')
                        if img_title == '':
                            img_src = content.get('src', '')
                            img_src = img_src.split('/')[-1].split('.', 1)[0]
                            try:
                                img_title = parse_emoji.softband_to_utf8(img_src)
                            except Exception as e:
                                print('解析表情失败，具体信息是{},{}'.format(e, comment))
                                img_title = ''
                        cont.append(img_title)

                    else:
                        if first_colon:
                            if content.find('：') == 0:
                                cont.append(content.replace('：', '', 1))
                                first_colon = False
                        else:
                            cont.append(content)

                wb_comment['comment_cont'] = ''.join(cont)
                wb_comment['comment_screen_name'] = comment.find(attrs={'class': 'WB_text'}).find('a').text

                wb_comment['comment_id'] = comment['comment_id']
                # TODO 将wb_comment.user_id加入待爬队列（seed_ids）
                wb_comment['user_id'] = comment.find(attrs={'class': 'WB_text'}).find('a').get('usercard')[3:]
                # todo 日期格式化
                wb_comment['create_time'] = comment.find(attrs={'class': 'WB_from S_txt2'}).text
            except Exception as e:
                print('解析评论失败，具体信息是{}'.format(e))
            else:
                yield wb_comment

        #此处有新老两种链接，如果为类似http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}&__rnd={}的以前的微博链接，此处就需要修改，把URL拼成这种格式，
        #若为比较新的微博，则URL为以下这种格式
        next_href = "https://weibo.com/aj/v6/comment/big?ajwvr=6&" + get_next_url(response.body)
        print "nexturl*****" + next_href
        yield scrapy.Request(next_href, callback=self.parse)


def get_html_cont(html):
    cont = ''
    data = json.loads(html, encoding='utf-8').get('data', '')
    if data:
        cont = data.get('html', '')

    return cont

def get_next_url(html):
    """
    获取下一次应该访问的url
    :param html:

    :return:
    """
    cont = get_html_cont(html)
    if not cont:
        return ''
    soup = BeautifulSoup(cont, 'html.parser')
    url = ''
    if 'comment_loading' in cont:
        url = soup.find(attrs={'node-type': 'comment_loading'}).get('action-data')

    if 'click_more_comment' in cont:
        url = soup.find(attrs={'action-type': 'click_more_comment'}).get('action-data')
    return url

