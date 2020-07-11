import re
import rsa
import time
import json
import string
import base64
import random
import binascii
import requests
import threading
import urllib.parse
from lxml import etree

zhanghao=''
mima=''
class Weibo():

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"})
        self.session.get("http://weibo.com/login.php")
    # 加密用户名
    def get_username(self):
        username_quote = urllib.parse.quote_plus(zhanghao)
        self.username_base64 = base64.b64encode(username_quote.encode("utf-8")).decode("utf-8")
    # 获取json重要
    def get_json_data(self):
        params = {
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": self.username_base64,
            "_": int(time.time() * 1000),
        }
        try:
            response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)
            self.json_data = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))
        except:
            pass
    # 加密密码
    def get_password(self):
        string = (str(self.json_data["servertime"]) + "\t" + str(self.json_data["nonce"]) + "\n" + str(mima)).encode(
            "utf-8")
        public_key = rsa.PublicKey(int(self.json_data["pubkey"], 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        self.password = binascii.b2a_hex(password).decode()
    # 获取验证码
    def yzm(self):
        # if self.json_data["showpin"] == 1:
        url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), self.json_data["pcid"])
        # print('请点击此网站查看验证码\n' + url)
        r = self.session.get(url)
        with open("验证码.jpeg", "wb") as fp:
            fp.write(r.content)
        weibo.main('',
                   '',
                   '验证码.jpeg',
                   "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload",
                   '1',
                   '8',
                   '1001',
                   '')
    # 开始登录
    def main(self, api_username, api_password, file_name, api_post_url, yzm_min, yzm_max, yzm_type, tools_token):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            # 'Content-Type': 'multipart/form-data; boundary=---------------------------227973204131376',
            'Connection': 'keep-alive',
            'Host': 'v1-http-api.jsdama.com',
            'Upgrade-Insecure-Requests': '1'
        }

        files = {
            'upload': (file_name, open(file_name, 'rb'), 'image/png')
        }

        data = {
            'user_name': api_username,
            'user_pw': api_password,
            'yzm_minlen': yzm_min,
            'yzm_maxlen': yzm_max,
            'yzmtype_mark': yzm_type,
            'zztool_token': tools_token
        }
        s = requests.session()
        # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
        r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False)
        self.code = r.json()['data']['val']
        # print(self.code)
    # 开始登录
    def login_pc(self):
        weibo.get_username()
        weibo.get_json_data()
        weibo.get_password()
        # weibo.yzm()
        post_data = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": self.json_data["rsakv"],
            "servertime": self.json_data["servertime"],
            "nonce": self.json_data["nonce"],
            "su": self.username_base64,
            "sp": self.password,
            "returntype": "TEXT",
        }

        post_data["pcid"] = self.json_data["pcid"]
        # post_data["door"] = self.code

        # login weibo.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        if json_data_1["retcode"] == "0":
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.18)",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time() * 1000),
            }
            response = self.session.get("https://passport.weibo.com/wbsso/login", params=params)
            json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                print('电脑网页版本登录成功\n此账号的id为：' + str(self.user_uniqueid) + '\n' + '此账号的名字为：' + self.user_nick)
                print('----------------------让我看看有多少憨批抢红包----------------------')
                weibo.red()
            else:
                print('登录失败')
        else:
            print('登录失败')

    def red(self):
        self.name=[]
        self.uid=[]
        url1='https://mall.e.weibo.com/redenvelope/receivedetail?set_id={}&page=1'.format(red_id)
        res1=self.session.get(url1)
        html = etree.HTML(res1.text)
        page = html.xpath('//div[@class="W_pages"]/a[contains(@class, "page S_txt1")]/text()')
        for i in range(1,int(page[-1])+1):
            url='https://mall.e.weibo.com/redenvelope/receivedetail?set_id={}&page={}'.format(red_id,i)
            res=self.session.get(url)
            html = etree.HTML(res.text)
            names = html.xpath('//div[@class="detail_list_wrap"]/ul[@class="detail_list"]/li/div/p/a/text()')
            uids = html.xpath('//div[@class="detail_list_wrap"]/ul[@class="detail_list"]/li/div/p/a/@href')
            for name,ids in zip(names,uids):
                uid=re.sub('https://weibo.com/u/','',ids)
                self.name.append(name)
                self.uid.append(uid)
                print(name,uid)
        # print('有'+len(self.uid)+'憨批抢了红包')

    def login_phone(self):
        self.session1 = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Host": "passport.weibo.cn",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "277",
            "Origin": "https://passport.weibo.cn",
            "Connection": "close",
            "Referer": "https://passport.weibo.cn/signin/login?aa=up&entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2Fcompose%2F",
            # "Cookie": "_T_WM=34960953895; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; SUB=_2A25z-Y5rDeRhGeFP71IT8i_PzTiIHXVRBRIjrDV6PUJbkdAKLUfakW1NQTCisV_P96T17vL4mzRhMsMo65nm8tmU; SUHB=0M2FLY7UiEA8iA; SCF=AurS26a9fa0FvAM2SAMPd2IcJit7440jFPB-KGRZ4grN6f9litMzc8NYU3yxRb7rq-Z1wBsrY9TgtcEptdzSTzc.; SSOLoginState=1593703995"
        }
        data = {
            'username': zhanghao,
            'password': mima,
            'savestate': '1',
            'r': 'https://m.weibo.cn/compose/',
            'ec': '1',
            'pagerefer': 'https%3A%2F%2Fm.weibo.cn%2Flogin%3FbackURL%3Dhttps%253A%252F%252Fm.weibo.cn%252Fcompose%252F',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': '',
        }
        url = 'https://passport.weibo.cn/sso/login'
        res = self.session1.post(url, headers=headers, data=data)
        if int(res.json()['retcode']) == 20000000:
            print('手机网页版本登录成功')
            while (True):
                print('----------------------年轻人做出你的选择----------------------')
                print('1.点赞      2.评论      3.转发')
                key = input('请输入对应的选项')
                if int(key) == 1:
                    weibo.zan()
                elif int(key) == 2:
                    weibo.pinglun()
                elif int(key) == 3:
                    weibo.zhuanfa()
                else:
                    print('瞎J8乱输干嘛')
        else:
            print('登录失败')

    def zan(self):
        self.zan_name = []
        self.zan_uid = []
        url1 = 'https://m.weibo.cn/api/attitudes/show?id={}&page=1'.format(bid)
        res1 = self.session1.get(url1)
        max=res1.json()['data']['max']
        for i in range(1,int(max)+1):
            url='https://m.weibo.cn/api/attitudes/show?id={}&page={}'.format(bid,i)
            res = self.session1.get(url)
            try:
                for sj in res.json()['data']['data']:
                    id = sj['user']['id']
                    screen_name = sj['user']['screen_name']
                    self.zan_name.append(screen_name)
                    self.zan_uid.append(id)
            except:
                pass
            time.sleep(5)
        a=[int(u) for u in self.zan_uid]
        b=[int(t) for t in self.uid]
        for name, uid in zip(self.name, b):
            if uid not in a:
                print('@'+name)

    def pinglun(self):
        self.pinglun_name=[]
        self.pinglun_uid=[]
        x='0'
        url='https://m.weibo.cn/comments/hotflow?id={}&mid={}'.format(bid,bid)
        res=self.session1.get(url)
        for i in range(1,int(res.json()['data']['max'])+1):
            url='https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(bid,bid,x)
            res=self.session1.get(url)
            try:
                x=res.json()['data']['max_id']
                for sj in res.json()['data']['data']:
                    id=sj['user']['id']
                    screen_name=sj['user']['screen_name']
                    self.pinglun_name.append(screen_name)
                    self.pinglun_uid.append(id)
            except:
                pass
            time.sleep(5)
        a=[int(u) for u in self.pinglun_uid]
        b=[int(t) for t in self.uid]
        for name, uid in zip(self.name, b):
            if uid not in a:
                print('@'+name)

    def zhuanfa(self):
        self.zhuanfa_name = []
        self.zhuanfa_uid = []
        url1 = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1'.format(bid)
        res1 = self.session1.get(url1)
        max=res1.json()['data']['max']
        for i in range(1,int(max)+1):
            url='https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'.format(bid,i)
            res = self.session1.get(url)
            for sj in res.json()['data']['data']:
                id = sj['user']['id']
                screen_name = sj['user']['screen_name']
                self.zhuanfa_name.append(screen_name)
                self.zhuanfa_uid.append(id)
            time.sleep(5)
        a=[int(u) for u in self.zhuanfa_uid]
        b=[int(t) for t in self.uid]
        for name, uid in zip(self.name, b):
            if uid not in a:
                print('@'+name)

if __name__ == "__main__":
    red_ids=input('请输入红包的链接')
    red_id=re.findall("\d+",red_ids)[-1]
    bids=input('请输入博文的链接')
    bid=re.findall("\d+",bids)[-1]
    print('----------------------开始运行----------------------')
    weibo = Weibo()
    weibo.login_pc()
    weibo.login_phone()