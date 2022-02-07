import random
import string


def girlfriend():
    count = 0
    name = ""
    while name != "xiaoLi":
        count += 1
        print(f"第{count}次请客送花，看电影.白找了{name}")
        name = 'xia' + (''.join(random.sample(string.ascii_letters, 3)))
    print(f"wa,终于找到你{name}")




