from urllib import request
from urllib import error
import re
import os
from Excel import ExcelOper
from SqliteImpl import SqliteImpl
from MySQLImpl import MySQLImpl
from SqlalchemyImpl import SqlalchemyImpl

class Scheduler(object):

    def __init__(self, url, user_agent):
        self.url = url
        self.headers = {'User-Agent': user_agent}
        self.excel_obj = ExcelOper()
        self.sqlite = SqliteImpl()
        #self.mysql = MySQLImpl()
        self.orm = SqlalchemyImpl()

    def read_html(self, codec):
        '''[read_html]
        
        [读取html页面内容]
        
        Arguments:
            url {[string]} -- [url地址]
            headers {[dict]} -- [用户代理，这里是一个字典类型]
            codec {[string]} -- [编码方式]
        
        Returns:
            [string] -- [页面内容]
        '''
        # 构建一个请求对象
        try:
            req = request.Request(self.url, headers=self.headers)
            # 打开一个请求
            response = request.urlopen(req)
            # 读取服务器返回的页面数据内容
            content = response.read().decode(codec)

            return content

        except error.URLError as e:
            print(e.reason)
            return None       
        
    def match_element(self, content, pattern):
        '''[match_element]
        
        [匹配元素]
        
        Arguments:
            content {[string]} -- [文本内容]
            pattern {[object]} -- [匹配模式]

        Returns:
            [list] -- [匹配到的元素]
        '''
        # 匹配所有用户信息
        
        userinfos = re.findall(pattern, content)
        
        return userinfos
    def write_file(self, content):
        with open('./qiubai.txt', 'a+') as fp:
            fp.write(content + '\n')

    def get_content(self):
        content = self.read_html('utf-8')
        pattern = re.compile(r'<div class="article block untagged mb15[\s\S]*?class="stats-vote".*?</div>', re.S)
        if content:
            userinfos = self.match_element(content, pattern)
            infos = []
            if userinfos:
                pattern = re.compile(r'<a href="(.*?)".*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>', re.S)
                picture = re.compile(r'<div class="thumb">.*?src="(.*?)"', re.S)
                for userinfo in userinfos:
                    item = self.match_element(userinfo, pattern)
                    pictures = self.match_element(userinfo, picture)
                    try:
                        if item:
                            userid, name, content, num = item[0]
                            # 去掉换行符，<span></span>，<br/>符号
                            userid = re.sub(r'\n|<span>|</span>|<br/>', '', userid)
                            name = re.sub(r'\n|<span>|</span>|<br/>', '', name)
                            content = re.sub(r'\n|<span>|</span>|<br/>|\x01', '', content)
                            
                            if pictures:
                                path = './users/'
                                if not os.path.exists(path):
                                    os.makedirs(path)

                                request.urlretrieve('http:' + pictures[0], path + os.path.basename(pictures[0]))
                                infos.append((userid, name, int(num), content, pictures[0]))

                            else:
                                infos.append((userid, name, int(num), content, ' '))
                               
                    except Exception as e:
                        print(e)
                self.excel_obj.write_excel(infos)
                #self.mysql.insert_record(infos)
                #self.mysql.dump()
                self.orm.insert_record(infos)
                #self.orm.update_reocrd()

if __name__ == '__main__':
  url = 'https://www.qiushibaike.com'
  user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
  handle = Scheduler(url, user_agent)
  handle.get_content()
            
            
            


    