from selenium import webdriver
import time,re,requests,csv,os,socket
from lxml import etree
import os
import sys

from selenium.webdriver.remote.webelement import WebElement

socket.setdefaulttimeout(7)
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
from selenium.webdriver.common.action_chains import ActionChains
options = webdriver.ChromeOptions()
browser = webdriver.Chrome()
browser.maximize_window()
browser.get('https://weibo.com/u/6718757082/home?wvr=5')
print('您将有1分钟时间登陆......')
# time.sleep(7)
# browser.find_element_by_xpath('//*[@id="loginname"]').send_keys('18861560575')
# browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3in]/div[2]/div/put').send_keys('1364350280wsq')
time.sleep(60)
f = open(r'.\1.txt','r',encoding='utf-8-sig')
s = f.readlines()[0]
if os.path.exists(r'.\weibo_data_财经.csv'):
    os.remove(r'.\weibo_data_财经.csv')
f = open(r'.\weibo_data_财经.csv', 'w', encoding='utf-8-sig')
csv_writer = csv.writer(f)
csv_writer.writerow(['微博名', '性别', '所在地', '粉丝数', '联系方式', '简介'])
f.flush()
browser.find_element_by_xpath('//*[@id="plc_top"]/div/div/div[2]/input').send_keys(s)
time.sleep(1)
browser.find_element_by_xpath('//*[@id="plc_top"]/div/div/div[2]/a').click()
browser.find_element_by_xpath('//*[@id="pl_feedtop_top"]/div[3]/a').click()
time.sleep(1)
list_history = []
# browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/div[1.txt]/div/dl[2]/dd/input').clear()
# browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/div[1.txt]/div/dl[2]/dd/input').send_keys(s)
browser.find_element_by_xpath('//*[@id="radio05"]').click()
# move = browser.find_element_by_xpath('//*[@id="pl_user_filtertab"]/div[1.txt]/ul/li[2]/span')
# ActionChains(browser).move_to_element(move).perform()
browser.find_element_by_xpath('/html/body/div[7]/div[2]/div/div[2]/a[1]').click()
browser.find_element_by_xpath('/html/body/div[1]/div[2]/ul/li[2]/a').click()
proxies = {'http':'http://153.99.22.113'}
m = 1
while m<=50:
    html = browser.execute_script('return document.documentElement.outerHTML')
    parse_html = etree.HTML(html)
    people_src_list = parse_html.xpath('//div[@class="avator"]/a/@href')
    print(people_src_list)
    cookies = browser.get_cookies()
    url = "http:"
    session = requests.session()
    cookieJar = requests.cookies.RequestsCookieJar()
    for i in cookies:
        cookieJar.set(i["name"],i["value"])
    session.cookies.update(cookieJar)
    for i in people_src_list:
      try:
        url1 = str(url)+str(i)+"?ishot=1.txt"
        print("url1: ",url1)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
        html = session.get(url=url1,headers=headers,timeout=(5,5)).text
        socket.setdefaulttimeout(7)
        pattern = re.compile(r"oid']='(.*?)';")
        src = pattern.findall(html,re.S)[0]
        pattern = re.compile(r'class=\\"username\\">(.*?)<\\/h1>')
        result1 = pattern.findall(html,re.S)[0]
        print(result1)
        #已经收录过的用户不会再被收录
        if result1 in list_history:
            continue
        try:
            k = 2
            flag = 0
            while True:
                if(k>=20):
                    flag = 1
                    break
                pattern = re.compile(r'<strong class=\\"W_f1{}\\">(.*?)<\\/strong>'.format(k))
                list = pattern.findall(html, re.S)
                if len(list)>=2:
                   result2 = list[1]
                   print(result2)
                   break
                k+=2
            if flag==1 or int(result2)<1000:
                continue
        except:
            pass
        pattern_sex = re.compile(r'\\"icon_bed\\"><a><i class=\\"W_icon icon_pf_(.*?)\\"><\\/i>')
        try:
          text_sex = pattern_sex.findall(html,re.S)[0]
        except:
          print('no sex')
          continue
        if text_sex=='male':
            result_sex = '男'
        else:
            result_sex = '女'
        url2 = str(url)+"//weibo.com/"+str(src)+"/about"
        pattern1 = re.compile(r"page_id']='(.*?)';")
        src1 = pattern1.findall(html,re.S)[0]
        html = session.get(url2,timeout=(5,5)).text
        socket.setdefaulttimeout(7)
        pattern = re.compile('<title>(.*?)</title>')
        t = pattern.findall(html,re.S)[0]
        if(t=='404错误'):
            url2 = str(url)+"//weibo.com/p/"+str(src1)+"/info?mod=pedit_more"
            html = session.get(url2,timeout=(5,5)).text
            socket.setdefaulttimeout(7)
        print("url2: ",url2)
        # print(html)
    # browser.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[1.txt]/div[1.txt]/a').click()
    # windows = browser.window_handles
    # time.sleep(5)
    # browser.switch_to.window(windows[-1.txt])
    # js = 'var q=document.documentElement.scrollTop={}'.format(500)
    # browser.execute_script(js)
    # html = browser.execute_script('return document.documentElement.outerHTML')
    # print(html)
    # browser.find_element_by_css_selector("[class='WB_cardmore S_txt1 S_line1 clearfix']").click()   #还要泛化
    # time.sleep(2)
    # js = 'var q=document.documentElement.scrollTop={}'.format(500)
    # browser.execute_script(js)
    # html = browser.execute_script('return document.documentElement.outerHTML')
        #需要一个数据清洗函数和可行的正则表达式
        # print(html)
        pattern = re.compile(r'<span class=\\"pt_title S_txt2\\">(.*?)<\\/span>.*?<span class=\\"pt_detail\\">(.*?)<\\/span>')
        ss = pattern.findall(html,re.S)
        result3 = ''
        result_location = ''
        result_intro = ''
        for z in range(len(ss)):
           if ('QQ' in ss[z][0]) or ('电话' in ss[z][0]) or ('微信' in ss[z][0]) or ('邮箱' in ss[z][0]):
              result3+=str(ss[z][0])+str(ss[z][1])+" "
           elif '所在地' in ss[z][0]:
              result_location+=str(ss[z][0])+str(ss[z][1])
           elif '简介' in ss[z][0]:
               result_intro += str(ss[z][0]) + str(ss[z][1])
        if result3=='':
            result3 = '无'
        if result_location=='':
            result_location = '无'
        if result_intro=='':
            result_intro = '无'
        print(result3)
        # result_intro = ''
        # pattern_intro = re.compile(r'<p class=\\"p_txt\\">(.*?)<\\/p>')
        # try:
        #     result_intro = pattern_intro.findall(html,re.S)[0]
        # except:
        #     result_intro = '无'
        csv_writer.writerow([result1,result_sex,result_location,result2,result3,result_intro])
        f.flush()
        list_history.append(result1)
        # time.sleep(1.txt)
      except:
        continue
    browser.find_element_by_class_name('next').click()
    m+=1
    # time.sleep(1)
# if os.path.exists(r'.\weibo_data_金融.csv'):
#     os.remove(r'.\weibo_data_金融.csv')
# f = open(r'.\weibo_data_金融.csv', 'w', encoding='utf-8-sig')
# csv_writer = csv.writer(f)
# csv_writer.writerow(['微博名', '性别', '所在地', '粉丝数', '联系方式', '简介'])
# f.flush()
# browser.find_element_by_xpath('//*[@id="pl_feedtop_top"]/div[3]/a').click()
# browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/div[1.txt]/div/dl[2]/dd/input').clear()
# browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/div[1.txt]/div/dl[2]/dd/input').send_keys('金融')
# browser.find_element_by_xpath('/html/body/div[8]/div[2]/div/div[2]/a[1.txt]').click()
# time.sleep(2)
# proxies = {'http':'http://153.99.22.113'}
# m = 1.txt
# while m<=50:
#     html = browser.execute_script('return document.documentElement.outerHTML')
#     parse_html = etree.HTML(html)
#     people_src_list = parse_html.xpath('//div[@class="avator"]/a/@href')
#     print(people_src_list)
#     cookies = browser.get_cookies()
#     url = "http:"
#     session = requests.session()
#     cookieJar = requests.cookies.RequestsCookieJar()
#     for i in cookies:
#         cookieJar.set(i["name"],i["value"])
#     session.cookies.update(cookieJar)
#     for i in people_src_list:
#       try:
#         url1 = str(url)+str(i)+"?ishot=1.txt"
#         print("url1: ",url1)
#         headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
#         html = session.get(url=url1,headers=headers,timeout=(5,5)).text
#         socket.setdefaulttimeout(7)
#         pattern = re.compile(r"oid']='(.*?)';")
#         src = pattern.findall(html,re.S)[0]
#         pattern = re.compile(r'class=\\"username\\">(.*?)<\\/h1>')
#         result1 = pattern.findall(html,re.S)[0]
#         print(result1)
#         #已经收录过的用户不会再被收录
#         if result1 in list_history:
#             continue
#         try:
#             k = 2
#             flag = 0
#             while True:
#                 if(k>=20):
#                     flag = 1.txt
#                     break
#                 pattern = re.compile(r'<strong class=\\"W_f1{}\\">(.*?)<\\/strong>'.format(k))
#                 list = pattern.findall(html, re.S)
#                 if len(list)>=2:
#                    result2 = list[1.txt]
#                    print(result2)
#                    break
#                 k+=2
#             if flag==1.txt or int(result2)<1000 or int(result2)>10000:
#                 continue
#         except:
#             pass
#         pattern_sex = re.compile(r'\\"icon_bed\\"><a><i class=\\"W_icon icon_pf_(.*?)\\"><\\/i>')
#         try:
#           text_sex = pattern_sex.findall(html,re.S)[0]
#         except:
#           print('no sex')
#           continue
#         if text_sex=='male':
#             result_sex = '男'
#         else:
#             result_sex = '女'
#         url2 = str(url)+"//weibo.com/"+str(src)+"/about"
#         pattern1 = re.compile(r"page_id']='(.*?)';")
#         src1 = pattern1.findall(html,re.S)[0]
#         html = session.get(url2,timeout=(5,5)).text
#         socket.setdefaulttimeout(7)
#         pattern = re.compile('<title>(.*?)</title>')
#         t = pattern.findall(html,re.S)[0]
#         if(t=='404错误'):
#             url2 = str(url)+"//weibo.com/p/"+str(src1)+"/info?mod=pedit_more"
#             html = session.get(url2,timeout=(5,5)).text
#             socket.setdefaulttimeout(7)
#         print("url2: ",url2)
#         pattern = re.compile(r'<span class=\\"pt_title S_txt2\\">(.*?)<\\/span>.*?<span class=\\"pt_detail\\">(.*?)<\\/span>')
#         ss = pattern.findall(html,re.S)
#         result3 = ''
#         result_location = ''
#         result_intro = ''
#         for z in range(len(ss)):
#            if ('QQ' in ss[z][0]) or ('电话' in ss[z][0]) or ('微信' in ss[z][0]) or ('邮箱' in ss[z][0]):
#               result3+=str(ss[z][0])+str(ss[z][1.txt])+" "
#            elif '所在地' in ss[z][0]:
#               result_location+=str(ss[z][0])+str(ss[z][1.txt])
#            elif '简介' in ss[z][0]:
#               result_intro+=str(ss[z][0])+str(ss[z][1.txt])
#
#         if result3=='':
#             result3 = '无'
#         if result_location=='':
#             result_location = '无'
#         if result_intro=='':
#             result_intro = '无'
#         print(result3)
#         # result_intro = ''
#         # pattern_intro = re.compile(r'<p class=\\"p_txt\\">(.*?)<\\/p>')
#         # try:
#         #     result_intro = pattern_intro.findall(html,re.S)[0]
#         # except:
#         #     result_intro = '无'
#         csv_writer.writerow([result1,result_sex,result_location,result2,result3,result_intro])
#         f.flush()
#         list_history.append(result1)
#         time.sleep(1.txt)
#       except:
#         continue
#     browser.find_element_by_class_name('next').click()
#     m+=1.txt
#     time.sleep(1.txt)
print('数据收录完毕。。。。。')