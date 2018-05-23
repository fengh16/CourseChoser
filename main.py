# The Data Used For Login & Choosing Course
# By fengh16, 17.09.20 18:58

from Settings import *
import time
import random
import re
import requests
import win32api
import win32con
import os
from bs4 import BeautifulSoup

s = requests.Session()
s.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Encoding':'gzip, deflate, br',
             'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'}

def sleepSometime():
    num = random.normalvariate(1, 1)
    while num <= 0.5:
        num = random.normalvariate(1, 1)
    time.sleep(num)


def downloadPicture():
    global mCode
    image = s.get(mCaptchaWebSite).content
    imagefile = open(mCaptchaPath, 'wb')
    imagefile.write(image)
    imagefile.close()
    win32api.MessageBox(win32con.NULL, "请登陆", "登陆提示", win32con.MB_OK | win32con.MB_ICONINFORMATION)
    os.system('mspaint ' + mCaptchaPath)
    mCode = input('Please Input Captcha: ')


def login():
    global content, token
    # print(s.cookies) # 检查cookie有没有问题
    # print(s.cookies.get_dict()) # 将cookie 转化成字典
    # s.cookies.set('a', 'b') # 将a的值设置成b
    s.cookies.clear() # 清空cookies
    s.get(mLogInWebSite)
    downloadPicture()
    data = {'j_username': mUserName,
            'j_password': mPassword,
            'captchaflag': 'login1',
            '_login_image_': mCode}
    res = s.post(mLogInPost, data)
    res.encoding = mWebDecoding
    content = res.text
    # print(content)
    error = re.findall(r'<div align="center">(.*?)</div>', content, re.S)
    if len(error) != 0:
        print('ERROR!')
        return False
    else:
        s.get(mChooseWebSiteFirstChoose)
        print('Login Success!')
        preForCheck()
        return True


def continueLogin():
    for i in range(50):
        if(login()):
            print("OK! Logged in!")
            break


def getToken():
    global content, token
    res = s.get(mChooseWebSiteRX)
    res.encoding = mWebDecoding
    content = res.text
    getTokenOnly()


def getTokenOnly():
    global content, token
    soup = BeautifulSoup(content, 'html.parser')
    token = soup.find_all('input', attrs={'name': 'token'})[0].get("value")


def satisfy(name, num):
    for block in mBlockList:
        if block[0] == name and block[1] == num:
            return False
    return True


def findBeforeChoose(mCourseNum):
    global content, token, mAlready
    getToken()
    findCourseData = {'m': 'rxSearch', 'page': '-1', 'token': '', 'p_sort.p1': '', 'p_sort.p2': '', 'p_sort.asc1': 'true',
                      'p_sort.asc2': 'true', 'p_xnxq': mNowState, 'is_zyrxk': '', 'tokenPriFlag': 'rx', 'p_kch': '',
                      'p_kcm': '', 'p_kkdwnm': '', 'p_kctsm': '', 'p_rxklxm': '', 'goPageNumber': '1'}
    findCourseData['p_kch'] = mCourseNum
    findCourseData['token'] = token
    res = s.post(mUrlBase, findCourseData)
    res.encoding = mWebDecoding
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    getTokenOnly()
    tr = soup.find_all('tr', attrs={'class': 'trr2'})
    for tr0 in tr:
        td = tr0.find_all('td')
        if int(td[4].text) != 0 and satisfy(td[1].text, td[2].text):
            # 有课余量
            submit(td[1].text, td[0].find_all('input')[0].get("value"))
            if td[1].text in mNeedCourses and checkChosen(td[3].text):
                mNeedCourses.remove(td[1].text)
                mAlready += td[1].text + "  "
                break
    preForCheck()


def submit(course, value):
    global content, token, mNowHit
    data = {'m': 'saveRxKc', 'page': '', 'token': '', 'p_sort.p1': '', 'p_sort.p2': '', 'p_sort.asc1': 'true',
            'p_sort.asc2': 'true', 'p_xnxq': mNowState, 'is_zyrxk': '', 'tokenPriFlag': 'rx', 'p_kch': '',
            'p_kcm': '', 'p_kkdwnm': '', 'p_kctsm': '', 'p_rxklxm': '', 'p_rx_id': '', 'goPageNumber': '1'}
    data['p_kch'] = course
    getTokenOnly()
    data['token'] = token
    data['p_rx_id'] = value
    res = s.post(mUrlBase, data)
    res.encoding = mWebDecoding
    content = res.text
    mNowHit += 1


def checkChosen(course):
    a = s.get(mChosenCourse)
    a.encoding = mWebDecoding
    b = a.text
    if course.strip() in b:
        return True
    return False


def preForCheck():
    global content, token
    res = s.get(mCheckLeft)
    res.encoding = mWebDecoding
    content = res.text


def checkLeft(course):
    global content, token
    getTokenOnly()
    data = {'m': 'kylSearch', 'page': '-1', 'token': '', 'p_sort.p1': '', 'p_sort.p2': '', 'p_sort.asc1': '',
            'p_sort.asc2': '', 'p_xnxq': mNowState, 'pathContent': '%BF%CE%D3%E0%C1%BF%B2%E9%D1%AF', 'p_kch': '',
            'p_kxh': '', 'p_kcm': '', 'p_skxq': '', 'p_skjc': '', 'goPageNumber': '1'}
    data['p_kch'] = course
    data['token'] = token
    res = s.post(mCheckBase, data)
    res.encoding = mWebDecoding
    content = res.text
    soup = BeautifulSoup(content, 'html.parser')
    getTokenOnly()
    tr = soup.find_all('tr', attrs={'class': 'trr2'})
    for tr0 in tr:
        td = tr0.find_all('td')
        print("查询结果： \t " + td[2].text + " \t " + td[1].text + " \t 课余量： " + td[4].text)
        if td[4].text != "0" and satisfy(td[0].text, td[1].text):
            return True



mTotalTry = 0
mNowHit = 0


while mNeedCourses.__len__() > 0:
    continueLogin()
    try:
        while mNeedCourses.__len__() > 0:
            print("开始循环遍历抢课列表！")
            for course in mNeedCourses:
                mTotalTry += 1
                print("共尝试：" + str(mTotalTry) + "\t次，成功：" + str(mNowHit) + "次，已抢到的列表：" + mAlready)
                if checkLeft(course):
                    findBeforeChoose(course)
                sleepSometime()
    except:
        print("Error Happened, need to login again!")
