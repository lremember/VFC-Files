# coding:utf-8
__author__ = 'MengYu'
"""
1. 本脚本用于爬取一个手机页面的所有电影url，可以稍加处理即可真正下载该页面的所有电影(提示：使用urlretrive保存带有.mp4的url即可)
2. 本脚本所使用的环境为python2.7，也可自行换成python3.5以上版本
3. 本脚本所使用的技术为：requests模块来访问页面，bs4来转换成HTML页面，再获取想要信息，selenium自动化技术操作Chrome浏览器，访问requests模块不能访问的iframe内联框架，设置请求头池来应对网站的反爬措施，如有需要或有钱，可以买点ip设置ip代理池，设置方法详见requests模块的设置代理的方法
4. 全局变量a是为了存储时给每一行标记序号，如不需要可自行去掉
5. 爬取速度完全由你的网速决定，你的网速越快，爬取越快，另外可以使用多线程的方法(可自行修改)
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
a = 1


class CrawlMovie(object):
    """爬取手机页面的电影"""
    def __init__(self):
        """初识化设置"""
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
            "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
            "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
            "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
            "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
            "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
            "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
            "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.chrome_options = Options()
        self.mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                                 "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
        # 由于是爬取手机页面，所以要设置Chrome为手机浏览器
        self.chrome_options.add_experimental_option("mobileEmulation", self.mobile_emulation)
        # 解决DevToolsActivePort文件不存在的报错
        self.chrome_options.add_argument('--no-sandbox')
        # 谷歌文档提到需要加上这个属性来规避bug
        self.chrome_options.add_argument('--disable-gpu')
        # 浏览器设置成无头模式，即无界面化，更方便
        self.chrome_options.add_argument('--headless')
        # 手动指定使用的浏览器位置(根据个人安装位置决定)
        self.chrome_options.binary_location = r"C:\Users\liuskyter\AppData\Local\Google\Chrome\Application\
        chrome.exe"
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

    def get_page(self, url):
        """获取页面，得到页面"""
        headers = {
            'User-Agent': random.choice(self.user_agent_list)
        }
        data = requests.get(url, headers=headers).content
        return data

    def parse_page(self, url):
        """将在get_page中获取的页面转换成HTML页面，再进行获取数据"""
        global a
        soup = BeautifulSoup(self.get_page(url))
        movie_list_soup = soup.find_all('a', attrs={'class': 'video-con video-con-tit ellipsis-1'})
        for i in movie_list_soup:
            url = 'http://vip.happyingbar.cn' + i.get('href')
            finally_url = self.parse_second(self.get_page(url))
            name = i.getText()
            info = name + ' : ' + finally_url

            with open('./movielist.txt', 'a+')as f:
                f.write(str(a) + ' ' +str(info) + '\n')
            print(a, info)
            a += 1
            break

    def parse_second(self, data):
        """由于真实电影页面有内联框架，故使用selenium进行模拟浏览器，方便转换iframe"""
        soup = BeautifulSoup(data)
        url = 'http://vip.happyingbar.cn' + soup.find_all('a', attrs={'class': 'pull-left'})[1].get('href')
        self.driver.get(url)
        print(u'开始爬取电影页面了')
        time.sleep(2)
        print self.driver.current_url
        # 转换到所要获取url所在的iframe框架
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="playleft"]/iframe'))
        time.sleep(0.5)
        # finally_url即目标url
        finally_url = self.driver.find_element_by_xpath('//*[@id="a1"]/video').get_attribute('src')
        print('finally url is', finally_url)
        return finally_url

    def run(self):
        # 试验：爬取一页的一个电影
        # url = 'http://vip.happyingbar.cn/vod/list-1.html'
        # self.parse_page(url)

        # 正式爬取
        for i in range(1, 24):
            url = 'http://vip.happyingbar.cn/vod/list-1-%s.html' % i
            self.parse_page(url)
        # 一定要关闭浏览器，否则会造成内存泄漏而死机
        self.driver.quit()


if __name__ == '__main__':
    CrawlMovie().run()
