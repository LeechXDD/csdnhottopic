import requests
import csv
import threading
url = 'https://www.csdn.net/api/articles?type=more&category=newarticles&shown_offset='
shown_offset = "1544240233000000"
data = []
tag = threading.Event()
def crawl(url):
    global  shown_offset
    try:
        req = requests.get(url + shown_offset)
    except:
        print('failed',req)
    content = req.json()

    shown_offset = str(content['shown_offset'])
    for item in content['articles']:
        if item['title'] not in data:
            data.append([item['title'],item['views'],item['user_name']])
            tag.set()



for i in range(3):
    t = threading.Thread(target=crawl,args=(url,))
    t.start()
    while threading.active_count()>1:
        tag.clear()
        tag.wait(3)
print(data)
with open('csdn.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['标题','阅读量','用户名'])
    for index in data:
        writer.writerow(index)
