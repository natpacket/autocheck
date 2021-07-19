# -*- coding:utf-8 -*-
import requests
import time
from hashlib import md5
import smtplib
import random
from email.mime.text import MIMEText

ss = requests.session()


class WXMsg:

    def __init__(self, corpid, secret, agentid):
        self.corpid = corpid
        self.secret = secret
        self.agentid = agentid
        self.access_token = None

    def get_token(self):
        access_token = None
        try:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
            params = {"corpid": self.corpid, "corpsecret": self.secret}
            resp = requests.get(url=url, params=params)
            # print(resp.text)
            access_token = resp.json().get('access_token')
            self.access_token = access_token
            # print(access_token)
        except Exception as e:
            print('error:', e)
        # pass
        return access_token

    def send_msg(self, title=None, content=None, touser='@all', toparty=None, access_token=None):
        if access_token is None:
            self.get_token()
            print(self.access_token)
            access_token = self.access_token
        url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        # print(url)
        payload = {
            "touser": touser,
            "toparty": toparty,
            # "totag": "TagID1 | TagID2",
            "msgtype": "textcard",
            "agentid": self.agentid,
            "textcard": {
                "title": title,
                "description": content,
                "url": "URL",
                "btntxt": ""
            },
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url=url, json=payload)
        print(resp.text)


# 登录
def login(user, passwd):
    payload = {"account": user, "password": md5(passwd.encode('utf8')).hexdigest()}
    # print(payload)
    res = ss.post(url="https://work.cninct.com/MBORequest?op=Login", json=payload)
    ret_json = res.json()
    user_id = ret_json["ext"]["userid"]
    print(user_id)
    return user_id


# 打卡
def check(user_id, login_dev):
    check_time = time.strftime("%H:" + str(random.randint(35, 55)) + ":%S", time.localtime())
    # print(check_time)
    # login_dev='iPhoneiPhone XR<iPhone11,8>'
    #          iPhoneiPhone XR<iPhone11,8>
    # login_dev = "microsoftmicrosoft"
    # check_time = "19:26:35"
    check_date = time.strftime("%Y-%m-%d", time.localtime())
    # check_date = "2021-05-08"
    payload = {"details_attend_longitude": "103.991464", "details_attend_latitude": "30.633447",
               "details_attend_date": check_date, "details_attend_time": check_time, "details_attend_name": "成都总部",
               "login_dev": login_dev}
    # print(payload)
    check_url = f"https://work.cninct.com/SUITANGOA?op=UploadAttendDetails&userid={user_id}"
    res = ss.post(url=check_url, json=payload)
    ret_json = res.json()
    print(ret_json)
    return ret_json['message']


def main():
    corpid = input('公司id:')
    secret = input('微信接口密文:')
    agentid = input('微信应用id:')
    toparty = input('部门id:')
    user = input('账号:')
    passwd = input('密码:')
    login_dev = input('登录设备:')
    # print(login_dev)
    login_dev = login_dev.replace('\'', '')
    # user_id = login(user, passwd)
    # message = check(user_id, login_dev)
    message = 'test'
    wx = WXMsg(corpid, secret, agentid)
    content = f'*{user}*的签到状态:{message} '+login_dev+' '+passwd
    print(content)
    wx.send_msg(title='隧唐签到结果', content=content, toparty=toparty)


if __name__ == '__main__':
    main()
