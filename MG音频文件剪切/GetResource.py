#encoding:utf-8
import re,os
from urllib import request
if os.path.exists('./received') == False:
    os.mkdir('./received')
with open("url.txt", "r") as f:
    files = f.read()
    print(files)
    url_list = re.findall(r'"(https{0,1}.+?)"',files)
    print(url_list)
    print(len(url_list))
    num = 0
    received_list = []
    for i in url_list:
        url = i.replace("\n",'')
        url_path = url.split('/')
        url_right_path = url_path[-1]
        url_left_path = url_right_path.split('?')
        if re.match(r'[\w\-]+\.\w+',url_left_path[0]) and ":" not in url_left_path[0] and url_left_path[0] not in received_list:
            doc_name = url_left_path[0]
            if len(url_left_path) > 1:
                url = url.replace("?"+url_left_path[-1],"")
            print(url,doc_name)
            try:
                request.urlretrieve(url, 'received/' + doc_name)
                num += 1
            except:
                pass
            received_list.append(doc_name)
    print(num)