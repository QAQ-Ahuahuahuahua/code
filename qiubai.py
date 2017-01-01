# coding : UFT-8
import requests
import csv
import random
import time
import socket
import http.client
import os
from bs4 import BeautifulSoup

def get_info( url, data = None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    }
    timeout = random.choice(range(60,180))
    while True :
        try:
            rep = requests.get(url, headers = header, timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:',e)
            time.sleep(random.choice(range(8,15)))
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text

def get_data(html ):
    final = []
    pictures = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    content_left = body.find(id = 'content-left') #找到该页总框
    contents = content_left.find_all('div',class_ = 'article block untagged mb15')#找到所有内容框
    pages = content_left.find('ul',class_ = 'pagination')#找到翻页框
    next_page = pages.find('span',class_= 'next')#找到下一页
    nextUrl = next_page.find_parent('a').get('href')


    for content in contents: #对每个故事进行遍历
        temp = []
        author = content.find('div',class_='author clearfix')
        picture = author.find('img')
        picture_src = picture.get('src')
        pictures.append(picture_src)
        user_name = content.find("h2").string
        temp.append(user_name)
        data = content.find(class_ = 'content')
        story = data.find('span').get_text()
        temp.append(story)
        numbers = content.find_all('i', class_ = 'number')
        good = numbers[0].string + '好笑'
        temp.append(good)
        comment = numbers[1].string + '评论'
        temp.append(comment)
        temp.append(picture_src)
        final.append(temp)

    return final,pictures,nextUrl

def page_turn( url):
    results_list = [] #百科信息
    pictures_list = [] #头像
    currentUrl = url
    count = 1
    while count <=3:
        html = get_info(currentUrl)
        results,pictures,nextUrl = get_data(html)
        results_list.append(results)
        pictures_list.append(pictures)
        currentUrl = url + nextUrl[1:]
        print(currentUrl)
        count = count +1
    return results_list,pictures_list

def write_data(datas, name):
    file_name = name
    for data in datas:
        with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def download_pic(imgs):
    count = 1
    if not os.path.exists('pic'):
        os.makedirs('pic')
    for pictures in imgs:
        for picture in pictures:
            if picture == '/static/images/thumb/anony.png?v=b61e7f5162d14b7c0d5f419cd6649c87':
                print("静态图片")
                continue
            else:
                try:
                    r = requests.get(picture)
                except BaseException as e:
                    print("图片下载失败", e)
                    time.sleep(random.choice(range(30, 80)))
                else:
                    filename = str(count) + '.jpg'
                    path = "pic/" + filename
                    f = open(path, 'wb')
                    f.write(r.content)
                    print(count)
                    count = count + 1


if __name__ == '__main__':
    url ='http://www.qiushibaike.com/'
    result,picture = page_turn(url)
    write_data(result, 'qiubai.csv')
    download_pic(picture)


