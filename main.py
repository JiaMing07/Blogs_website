# This is a sample Python script.
import os
import requests
import IPython
import json
import pymysql
from IPython import embed
from bs4 import BeautifulSoup as BS
import logging
from time import sleep
import time
import re
from lxml import etree
import parsel
import random

fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler("crawler2.log", encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
# logger.addHandler(console)

ua = "Mozilla/5.0 (compatible; Baiduspider/2.0; + http://www.baidu.com/search/spider.html)"
cookie = "PHPSESSID=dcc4a625a040dd4b46cb64a621fb03fe; _ga=GA1.1.2018851768.1661700213; csrfToken=DRmGzdTr3ohi6lEvvcYMxW9N; __gads=ID=b4a4c1b795db5a4f-22df497ddcd5008a:T=1661706204:RT=1661706204:S=ALNI_MYEBjZpTsDvYnKgAeMKs7EnLcMSWg; __gpi=UID=0000092e45c608b3:T=1661706204:RT=1661706204:S=ALNI_MaUnCIsDZQMmFb-EQu896XvwI2H3Q; _ga_MJYFRXB3ZX=GS1.1.1661706200.2.1.1661707762.0.0.0; isCloseBeginnerGuide=1"
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"


def get_user_agent_pc():
    user_agent_pc = [
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.71 '
        'Safari/537.36',
        'Mozilla/5.0.html (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.html.1271.64 '
        'Safari/537.11',
        'Mozilla/5.0.html (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) '
        'Chrome/10.0.html.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 '
        'Safari/537.36',
        "Mozilla/5.0 (compatible; Baiduspider/2.0; + http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
    ]
    return random.choice(user_agent_pc)


def get_url_list(keyword):
    print(keyword)
    url_list = []
    for page in range(1, 44):
        sleep(1)
        print(page)
        try:
            resp = requests.get(f"https://segmentfault.com/search?q={keyword}&type=article&page={page}",
                                headers={'user-agent': ua})
        except Exception as e:
            embed(header=str(e))
        else:
            soup = BS(resp.text.encode('raw_unicode_escape').decode(), 'lxml')
            urls = soup.find_all('li', class_='list-group-item')
            base_url = "https://segmentfault.com"

            for url in urls:
                url = url.find("a").get('href')
                url = base_url + str(url)
                url_list.append(url)
                # print(url)
            if keyword == "C%23":
                # 当 keyword = "C%23" 时使用下面的语句
                f = open(f'./url_list/C#.txt', 'w+', encoding='utf-8')
            else:
                f = open(f'./url_list/{keyword}.txt', 'w+', encoding='utf-8')
            for url in url_list:
                f.write(url)
                f.write("\n")
    # return url_list


def get_blog(url_list, keyword):
    base_url = "https://segmentfault.com"
    num = 480
    pic_num = 0
    author_pic_num = 0
    for idx in range(num, 860):
        num = num + 1
        print(num)
        url = url_list[idx]
        print(url)
        sleep(2)
        i = url[27:]
        get_article = False
        get_src = False
        ua = get_user_agent_pc()
        try:
            resp = requests.get(url, headers={'user-agent': ua, 'cookie': cookie})
            # resp.raise_for_status()
        except Exception as e:
            print(e)
        else:
            soup = BS(resp.text.encode('raw_unicode_escape').decode(), 'lxml')
            title = soup.find('h1', class_='h2 mb-3')
            if title is not None:
                title = title.find('a').string
                # print(title)
                article = soup.find('article')
                if article is not None:
                    # print(article)
                    get_article = True
                if get_article:
                    text = article.text
                    if len(str(article.text)) > 60:
                        show_text = str(article.text)[0:60]
                        show_text = show_text.replace("\n", " ")
                        show_text = show_text + "..."
                    else:
                        show_text = str(article.text)
                    print(show_text)
                    imgs = article.find_all('img')
                    src_list = []
                    if not imgs:
                        get_src = True
                    for img in imgs:
                        has_src = img.get('src')
                        # if str(img['src'])[0]=='/':
                        #   img['src'] = base_url + str(img['src'])
                        if has_src is not None:
                            pic_num = pic_num + 1
                            if str(img['src']):
                                if str(img['src'])[0] == '/':
                                    print(has_src)
                                    pic_url = base_url + str(img['src'])
                                else:
                                    pic_url = str(img['src'])

                            get_src = True
                            pic_name = keyword + "_article_pic" + str(pic_num)
                            road = "img/" + pic_name + ".gif"
                            src = "/static/" + road
                            src_list.append(src)
                            try:
                                pic_resp = requests.get(pic_url, headers={'user-agent': ua, "cookie": cookie})
                            except Exception as e:
                                img['src'] = ""
                                logger.exception(f"{num};{e}")
                            else:
                                byte = pic_resp.content
                                print(src)
                                img['src'] = src
                                with open(f"./img/{pic_name}.gif", "wb") as f:  # 文件写入
                                    f.write(byte)
                                    time.sleep(0.5)

                    if get_src:
                        author_pic_num = author_pic_num + 1
                        author_pics = soup.find_all('picture', class_='rounded-circle')
                        author_pic = str(author_pics[0].find('img').get('src'))
                        author_pic_name = keyword + "_author_pic" + str(author_pic_num)
                        author_road = "img/" + author_pic_name + ".gif"
                        author_src = "/static/" + author_road
                        author_pic_resp = requests.get(author_pic, headers={'user-agent': ua, "cookie": cookie})
                        author_byte = author_pic_resp.content
                        with open(f"./img/{author_pic_name}.gif", "wb") as f:  # 文件写入
                            f.write(author_byte)
                            time.sleep(0.5)
                        author_img = author_pics[0].find('img')
                        author_img['src'] = author_src
                        author_pic = author_src
                        author_name = soup.find('div', class_='d-flex align-items-center mb-3')
                        author_name = author_name.find('a', class_='text-body')
                        author_name = author_name.string
                        author_popularity = soup.find('div', class_='me-4')
                        author_popularity = author_popularity.find('strong').string
                        author = soup.find_all('div', class_='d-flex align-items-center mb-3')
                        author = author[1].find_all('strong')
                        author_fans = author[1].string
                        like = soup.find('button', class_="btn me-2 rounded btn btn-outline-primary")
                        like = like.find_all('span')
                        # print(len(like))
                        if len(like) == 2:
                            like = like[1].string
                        else:
                            like = "0"
                        # print(like)
                        collect = soup.find('button', class_="btn me-2 rounded btn btn-outline-secondary")
                        collect = collect.find_all('span')
                        if len(collect) >= 2:
                            collect = collect[1].string
                        else:
                            collect = "0"
                        data = soup.find('div',
                                         class_='text-secondary font-size-14 mt-3 mb-5 d-flex flex-wrap justify-content-between')
                        data = data.find('div')
                        data = data.find_all('span')
                        data = str(data[0])
                        # print(re.search('-->(.*)<',data).group(1))
                        data = re.search('-->(.*)<', data).group(1)
                        read = str(data)
                        pub_date = soup.find('time')
                        pub_date = str(pub_date)
                        # print(re.search('-->(.*)<',pub_date).group(1))
                        pub_date = re.search('-->(.*)<', pub_date).group(1)
                        pub_date = str(pub_date)
                        if pub_date[-1] == '日':
                            print(re.search('(.*) 月 (.*) 日', pub_date).group(2))
                            month = re.search('(.*) 月 (.*) 日', pub_date).group(1)
                            month = str(month)
                            if len(month) <= 1:
                                month = "0" + month
                            day = re.search('(.*) 月 (.*) 日', pub_date).group(2)
                            day = str(day)
                            if len(day) <= 1:
                                day = "0" + day
                            pub_date = "2022-" + str(month) + "-" + str(day) + " "
                            # print('yes')
                        article = article.prettify()
                        article = article.replace("\n", "")
                        dic = {'title': title, 'article': article, 'text': text, 'author_pic': author_pic,
                               'author_name': author_name, 'author_src': author_src, 'src_list': src_list,
                               'author_popularity': author_popularity, 'author_fans': author_fans, 'like': like,
                               'collect': collect, 'read': read, 'pub_date': pub_date, 'url': url,
                               'show_text': show_text}
                        print(dic)
                        f = open(f'./data/{i}.json', 'w+', encoding='utf-8')
                        json.dump(dic, f, ensure_ascii=False, indent=4)
                        f.close()
                        if author_pic_num == 300:
                            break
            # print(pub_date)


def read_list(keyword):
    lst = []
    with open(f'./url_list/{keyword}.txt', "r", encoding="utf-8") as f:
        url_list = f.readlines()
        for url in url_list:
            url = url.replace("\n", "")
            lst.append(url)
    return lst


def get_list():
    lst = []
    base_url = "https://segmentfault.com/a/"
    file_lst = os.listdir("./data")
    for i in range(0, len(file_lst)):
        file_name = file_lst[i]
        file_name = base_url + file_name[0:-5]
        lst.append(file_name)
    f = open('./url_list/crawler.txt', 'w+', encoding='utf-8')
    for url in lst:
        f.write(url)
        f.write("\n")


def get_article(url_list):
    base_url = "https://segmentfault.com"
    num = 900
    for idx in range(num, len(url_list)):
        num = num + 1
        print(num)
        url = url_list[idx]
        print(url)
        sleep(1.2)
        id = url[27:]
        with open(f"./data/{id}.json", "r", encoding="utf-8") as t:
            old_data = json.load(t)
        get_article = False
        get_src = False
        ua = get_user_agent_pc()
        try:
            resp = requests.get(url, headers={'user-agent': ua, 'cookie': cookie})
            # resp.raise_for_status()
        except Exception as e:
            print(e)
        else:
            soup = BS(resp.text.encode('raw_unicode_escape').decode(), 'lxml')
            title = soup.find('h1', class_='h2 mb-3')
            if title is not None:
                title = title.find('a').string
                # print(title)
                article = soup.find('article')
                if article is not None:
                    # print(article)
                    get_article = True
                if get_article:
                    try:
                        codes = article.find_all("code")
                        imgs = article.find_all('img')
                        str_img_old = []
                        str_img_new = []
                        print(imgs)
                        cnt = 0
                        for img in imgs:
                            has_src = img.get('src')
                            if has_src is not None:
                                if img['src']:
                                    img['src'] = old_data['src_list'][cnt]
                                    cnt = cnt + 1
                        if codes:
                            str_codes_old = []
                            str_codes_new = []
                            for code in codes:
                                code = str(code)
                                str_codes_old.append(code)
                                code = code.replace("\n", "<br>")
                                str_codes_new.append(code)
                            articles = article.prettify()
                            for i in range(0, len(str_codes_old)):
                                articles = articles.replace(str_codes_old[i], str_codes_new[i])
                            for i in range(0, len(str_img_old)):
                                articles = articles.replace("/img/remote/1460000014706307?w=654&h=341", str_img_new[i])
                            print(articles)
                            articles = articles.replace("\n", "")
                            dic={}
                            dic['new_article'] = articles
                            id = id + "_1"
                            f = open(f'./datas/{id}.json', 'w+', encoding='utf-8')
                            json.dump(dic, f, ensure_ascii=False, indent=4)
                            f.close()
                        else:
                            article = article.prettify()
                            article = article.replace("\n", "")
                            dic = {}
                            dic['new_article'] = article
                            id = id +"_1"
                            f = open(f'./datas/{id}.json', 'w+', encoding='utf-8')
                            json.dump(dic, f, ensure_ascii=False, indent=4)
                            f.close()
                    except Exception as e:
                        logger.exception(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # search_list = ["python", "C++", "C%23", "Java", "JavaScript", "PHP", "SQL", "iOS"]
    # for key in search_list:
    #     get_url_list(key)
    # get_url_list("C%23")
    # get_url_list("Rust")
    # python_list = get_url_list("python")
    # url_lists = read_list("python")
    # get_blog(url_lists, "python")
    # 分开爬每个关键词的内容，记得更换read_list中的关键词参数
    # SQL_list = read_list("SQL")
    # get_blog(SQL_list, "SQL")
    # 重新爬取article的内容，保证排版
    crawler_list = read_list("crawler")
    get_article(crawler_list)
    # 检查再次爬取的内容是否完全
    file_list1 = os.listdir("./datas")
    print(len(file_list1))
    file_list3 = []
    for fi in file_list1:
        file_list3.append(fi[0:16])
    file_list2 = os.listdir("./data")
    file_list4 = []
    for fi in file_list2:
        file_list4.append(fi[0:16])
    file_list3 = sorted(file_list3)
    file_list4 = sorted(file_list4)
    for i in range(0, 299):
        if file_list3[i] != file_list4[i]:
            print(file_list3[i])
            print(file_list4[i])
            break
    # get_list()
    # crawler_list = read_list("crawler")
    # get_article(crawler_list)
    # get_blog(python_list)
    # lst = ["https://segmentfault.com/a/1190000021896573"]
    # get_blog(lst)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
