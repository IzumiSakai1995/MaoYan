#__author: Liu Zheng
#date:2018/6/29

from multiprocessing import Pool
import json
import requests
import re

def main(offset):
    url = 'http://maoyan.com/board/4?offset=0' + str(offset)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_in_file(item)
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    return response.text

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }

def write_in_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()
if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i * 10 for i in range(10)])
