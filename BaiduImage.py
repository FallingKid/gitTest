# coding=utf-8
import os
import requests
from urllib import parse
from functools import wraps

Word = '科比'
Page = 1
Headers = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
Path = '/home/zimoliang/图片/爬虫百度图片/{}/'.format(Word)
Name_repeat = {}


def get_page(pn):
    params = {'tn': 'resultjson_com', 'word': Word, 'pn': pn}
    url = 'https://image.baidu.com/search/index?' + parse.urlencode(params)
    try:
        response = requests.get(url, headers=Headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


# 生成器
def get_images(json_images):
    if json_images.get('data'):
        for image in json_images['data']:
            if image:
                title = image['fromPageTitleEnc']
                title = title.replace('/', '杠')
                url = image['hoverURL']
                yield {'title': title, 'url': url}


# 装饰器，打印下载图片名称
def log_saving(func):
    @wraps(func)
    def wrapper(image):
        print('下载 {}.jpg'.format(image['title']))
        func(image)

    return wrapper


@log_saving
def save_image(image):
    if not os.path.exists("{}".format(Path)):
        os.makedirs("{}".format(Path))
    try:
        response = requests.get(image['url'])
        if response.status_code == 200:
            path_image = "{0}/{1}.jpg".format(Path, image['title'])
            if not os.path.exists(path_image):
                with open(path_image, 'wb') as f:
                    f.write(response.content)
            # 对名字重复的图片，后面加上（1）、（2）...（...）
            else:
                Name_repeat[image['title']] = 1 if not Name_repeat.get(
                    image['title']) else Name_repeat[image['title']] + 1
                path_image = "{0}/{1}（{2}）.jpg".format(
                    Path, image['title'], Name_repeat[image['title']])
                with open(path_image, 'wb') as f:
                    f.write(response.content)
    except:
        print('\t{0}.jpg 下载失败'.format(image['title']))


def main():
    for i in range(1, Page + 1):
        json_images = get_page(i * 30)
        for image in get_images(json_images):
            save_image(image)


if __name__ == '__main__':
    main()
