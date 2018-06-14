# 功能
- 爬取新浪微博单条微博的评论信息：爬取评论信息，并写入数据库
- 后续会加入爬取某个人的所有微博信息


# 输入
微博id，例如新浪微博https://weibo.com/1638782947/Glid241mP?type=comment#_rnd1528963859032 ，参考https://github.com/SpiderClub/weibospider/wiki/%E5%BE%AE%E5%8D%9A%E8%AF%84%E8%AE%BA%E6%8A%93%E5%8F%96%E5%88%86%E6%9E%90%E8%BF%87%E7%A8%8B 通过chrome分析其请求内容URL为https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4250748880958571 ，即为我们的输入url

# 输出
- 用户昵称：如"Dear-迪丽热巴"
- 用户id：可用于后续爬取该用户的微博内容，对用户的行为进行分析
- 评论内容：用户具体的评论内容
- 创建时间

# 运行环境
- 开发语言：python2.7
- 系统： Windows/Linux

# 使用说明
1.安装scrapy框架
其中有一些坑，主要是windows下的twisted包 python-mysqldb之类的安装问题，可自行google解决；
```bash
$ git clone https://github.com/jsnjfz/weiboscrapy.git
```
将本项目下载到本地目录；<br>
2.把settings中的COOKIES配置改成你的用户登录以后的COOKIES；
把数据库配置改成你自己的数据库配置信息<br>
3.mysql建表，数据库和settings中的配置一致；
运行建表语句<br>
4.将"weibo.py"文件中的url_base根据输入中的方法调整成需要获取的url；<br>
5.进入项目目录下，运行scrapy crawl weibo即可进行爬取。

# 如何获取cookie
1.用Chrome打开<https://weibo.com>；<br>
2.按F12键打开Chrome开发者工具；<br>
3.点开“Network”，输入微博的用户名、密码，登录；<br>
4.点击Chrome开发者工具,点击"Headers"，其中"Request Headers"下，"Cookie"后的值即为我们要找的cookie值，复制即可

# 注意事项
- cookie有期限限制，大约有几天的有效期，超过有效期需重新更新cookie。

# 感谢
分析微博部分和部分源码参考了https://github.com/SpiderClub/weibospider
的内容,但由于原作者的框架搭建太庞大，于是根据scrapy框架写了个轻便的爬虫