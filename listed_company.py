# listed_company.py
# author:Bushang
# contact:bushang_zhan@163.com

import requests
import pymysql
import json
import time
import random

#连接数据库
dbconn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'use_your_password',
    database = 'listed_company',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

#该函数是从数据库中取出一个数据，后来在主函数中直接取出所有内容，直接遍历，因此该函数不再使用。
def get_com_code_from_db():
    try:
        with dbconn.cursor() as cursor:
            sql = 'SELECT code FROM company_list'
            cursor.execute(sql)
            #获取一家公司代码
            dict = cursor.fetchone()
            com_code = dict['code']
            return com_code
    except:
        print("数据库获取数据错误")

def get_html_text(com_code):
    #获取上交所A股公司页面内容
    if int(com_code)>=600000 and int(com_code) < 700000:
        #构造请求头，加入浏览器信息，模拟浏览器请求，可以自行增加删减。
        user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        ]
        #通过抓包分析，想要访问的页面需要跳转，因此要加referer。
        headers = {'referer':'http://www.sse.com.cn/', 'User-Agent':random.choice(user_agent)}
        url = 'http://query.sse.com.cn/commonQuery.do?sqlId=COMMON_SSE_ZQPZ_GP_GPLB_C&productid=' + com_code
        print(url)
        response = requests.get(url, headers = headers, timeout = 500)
        #抓取过程中，经常出现[WinError 10060]错误，通过分析，应该是服务器方不稳定造成的。
        # 因此每爬一个数据，随机休息0~3秒，模拟用户访问。
        time.sleep(random.randint(0,3))
        if response.status_code == 200:
            # print(response.text)
            return response.text
        else:
            print("页面链接错误")
    #如果要爬取深交所的页面内容，可以在这里补充代码，我这里没用到。
    else:
        print("深圳公司")

def parse_page(page_text):
    #获取的页面为json字符串，在这里通过json.loads转为字典数据结构。
    page_text_dict = json.loads(page_text)
    #通过分析，取出字典中所需要的字段。
    result = page_text_dict["result"]
    com_data_list = result[0]
    #下面两行代码，遍历所有字段，并取出需要的字段。
    com_data_key = {'SECURITY_CODE_A','COMPANY_ABBR','AREA_NAME_DESC','CSRC_CODE_DESC','LEGAL_REPRESENTATIVE'}
    com_data = {key:value for key,value in com_data_list.items() if key in com_data_key}
    return com_data

def save_data_to_db(com_data):
    with dbconn.cursor() as cursor:
        #带变量的数据写入数据库，别忘记加commit
        sql = 'INSERT INTO crawl_list_sh1_copy(SECURITY_CODE_A,COMPANY_ABBR,AREA_NAME_DESC,CSRC_CODE_DESC,LEGAL_REPRESENTATIVE) VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(sql,(com_data['SECURITY_CODE_A'], com_data['COMPANY_ABBR'], com_data['AREA_NAME_DESC'], com_data['CSRC_CODE_DESC'], com_data['LEGAL_REPRESENTATIVE']))
        dbconn.commit()

def main():
    #构建循环
    with dbconn.cursor() as cursor:
        #从数据库中的code字段取出第一个数据到最后一个数据，18***代指到最后一个。
        # 使用limit的好处是，如果程序中断，可以更改0，从中断的位置继续获取数据，不用重头开始。
        sql = 'SELECT code FROM company_list LIMIT 0,18446744073709551615'
        cursor.execute(sql)
        codes = cursor.fetchall()
        print(codes)
        for com_code in codes:
            #从数据库中获取一个公司的代码
            #com_code = get_com_code_from_db()
            #抓取网页的内容
            page_text = get_html_text(com_code['code'])
            #解析网页，返回字典数据
            com_data = parse_page(page_text)
            #保存到数据库中
            save_data_to_db(com_data)

if __name__ == '__main__':
    main()
    #关闭数据库
    dbconn.close()