import requests
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
from selenium import webdriver
import time,os,csv,random,sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
f = open(r'.\1.txt',encoding="utf-8")
s = f.readlines()[0]
if os.path.exists(r'.\ending.csv'):
    os.remove(r'.\ending.csv')
f = open(r'.\ending.csv', 'w', encoding='utf-8-sig')
csv_writer = csv.writer(f)
csv_writer.writerow(['企业名', '注册日期', '注册资本', '法定代表人', '联系电话', '注册地址','经营范围'])
f.flush()
options = webdriver.ChromeOptions()
browser = webdriver.Chrome()
browser.maximize_window()
browser.get('https://www.tianyancha.com/login?from=https%3A%2F%2Fwww.tianyancha.com%2Fadvance%2Fsearch')
time.sleep(1)
browser.find_element_by_xpath("//*[@id='web-content']/div/div[2]/div/div/div[3]/div[3]/div[1]/div[2]").click()
browser.find_element_by_xpath("//*[@id='mobile']").send_keys("18591881286")
browser.find_element_by_xpath("//*[@id='password']").send_keys("huatai789")
browser.find_element_by_xpath("//*[@id='web-content']/div/div[2]/div/div/div[3]/div[3]/div[2]/div[4]").click()
time.sleep(10)
browser.find_element_by_xpath("//*[@id='keywordInput']").send_keys(s)
browser.find_element_by_xpath("//*[@id='web-content']/div/div/div[3]/div/div/div[2]").click()
try:
    browser.find_element_by_xpath("//*[@id='web-content']/div/div/div[3]/div/div/div[2]").click()
except:
    pass
time.sleep(5)
# html = browser.execute_script('return document.documentElement.outerHTML')
m = 1
while m<=250:
    html = browser.page_source
    parse_html = etree.HTML(html)
    for index in range(1,21):
       try:
        url = '//*[@id="web-content"]/div/div[2]/div[2]/div/div[1]/div[{}]/div/div[3]'.format(index)
        name = parse_html.xpath(url+'//a[@class="name  "]//text()')
        s_name = ""
        for i in name:
            s_name+=i
        person = parse_html.xpath(url+'//a[@class="legalPersonName link-click"]//text()')[0]
        #如果没找到，就判定该企业的标注略有不同（和绝大多数企业不同），那么直接抓下一个
        money = parse_html.xpath(url+'//div[@class="title -narrow text-ellipsis"]/span/text()')[0]
        date = parse_html.xpath(url+'//div[@class="title  text-ellipsis"]/span/text()')[0]
        try:
          telephone = parse_html.xpath(url+'//div[@class="col"]/span[2]/text()')[0]
        except:
          telephone='无'
        scope = parse_html.xpath(url+'//div[@class="match row text-ellipsis "]/span[2]//text()')
        s_scope = ""
        for i in scope:
          s_scope+=i
        if(s_scope==''):
            s_scope='无'
        #准备进企业主页拿地址信息（这里使用requests页面的切换太过耗时）
        href = parse_html.xpath(url+'//a[@class="name  "]/@href')[0]
        #拿到cookie
        cookies = browser.get_cookies()
        session = requests.session()
        cookieJar = requests.cookies.RequestsCookieJar()
        for i in cookies:
            cookieJar.set(i["name"],i["value"])
        session.cookies.update(cookieJar)
        html_href = session.get(url=href,headers=headers).text
        parse_html1 = etree.HTML(html_href)
        address = parse_html1.xpath('//div[@class="detail-content"]//text()')[0]
        address = address.strip()
        print(s_name,person,money,date,telephone,address,s_scope)
        csv_writer.writerow([s_name,date,money,person,telephone,address,s_scope])
        f.flush()
        time.sleep(random.uniform(1, 3))
       except:
        if(browser.current_url=="https://antirobot.tianyancha.com/captcha/verify?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fadvance%2Fsearch%2Fresult&rnd="):
            print('有一个验证页面需要解决，解决好了之后输入yes....')
            while True:
             str = input("请输入(yes):")
             if(str=='yes'):
                 break;
        continue
    browser.find_element_by_xpath('//a[@class="num -next"]').click()
    time.sleep(random.uniform(0,2))
