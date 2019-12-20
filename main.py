# -*- coding: utf-8 -*-
# @Time    : 2019-12-20 14:18
# @Author  : Lu Baogui
# @Email   : 15766972573@qq.com
# @File    : main.py
# @Software: PyCharm


import logging
import os
import requests
import urllib
import argparse
from tld import get_tld
from bs4 import BeautifulSoup

FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(filename='outer_links.txt', format=FORMAT, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def getHTMLText(url):
    '''
    获取网页的html文档
    '''
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text, True
    except Exception as e:
        return e, False


def main(url, tab):
    links = []
    links_inner = []
    links_outer = []
    demo, status = getHTMLText(url)
    domain = get_tld(url, as_object=True).fld

    if status:
        soup = BeautifulSoup(demo, 'html.parser')
        a_labels = soup.find_all('a', attrs={'href': True})
        for a in a_labels:
            if 'http' in a.get('href'):
                link = a.get('href')
            elif a.get('href')[0:1] == '/':
                link = tab + a.get('href')
            else:
                link = url + a.get('href')
            links.append(link)
            try:
                if domain == get_tld(link, as_object=True).fld:
                    links_inner.append(link)
                else:
                    links_outer.append(link)
            except Exception as e:
                links_outer.append(link)
            links.append(link)
        links = list(set(links))
        links_inner = list(set(links_inner))
        links_outer = list(set(links_outer))
    return links, links_inner, links_outer


def level_interface(urls):
    links_level_all = []
    links_inner_level = []
    links_outer_level = []
    for i in urls:
        try:
            tab = i.split('.com')[0] + '.com'
        except Exception as e:
            tab = i
        link_level, links_inner_level, links_outer_level = main(i, tab)
        links_level_all += link_level
        if links_outer_level:
            logging.info("主页：{} 外链：{}".format(i, links_outer_level))
    return links_level_all, links_inner_level, links_outer_level


if __name__ == "__main__":
    """

    运行命令： python main.py 'http://www.xxxx.xxxx/' 3

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url:", type=str)
    parser.add_argument("number", help="number for runs:", type=int)
    args = parser.parse_args()
    links_inner = list()
    links_inner.append(args.url)
    num = args.number

    logging.info(" ======= url: {};层级: {} =======".format(args.url, num))
    for i in range(num):
        logging.info(" ================= 目前处于第 {} 层 ==============".format(i))
        links, links_inner, links_outer = level_interface(links_inner)




