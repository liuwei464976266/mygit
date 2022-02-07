import requests, random, string, json


def Test(userName, nickName):
    url = 'http://192.168.10.212:9003/checkSensitiveWord'
    headers = {}
    payload = dict(userName=userName, nickName=nickName)
    response = requests.post(url, headers, payload)
    return response.text


def main():
    with open("blacklist.txt", "r", encoding='utf-8') as f:
        JJ = 0
        for i in f.readlines():
            Name = (''.join(random.sample(string.ascii_letters + string.digits, 9)))
            JJ += 1
            line = i.strip()
            line = (''.join(random.sample(string.ascii_letters + string.digits, 3)))+line
            print(line)
            if int(JJ) > 0:
                    res = Test(line, line)
                    res = json.loads(res)
                    print(JJ)
                    if res['nickName'] is False or res['userName'] is False:
                        print(line, line, res)
                        with open('error.txt', 'a', encoding='utf-8') as f:
                            f.write(str(line) + '----' + str(res) + '\n')



# main()
# a = Test('yin', 'yi n')
# print(a)


name = 'JKDHEWASWQQA'

with open("blacklist.txt", "r", encoding='utf-8') as f:
    JJ = 0
    for i in f.readlines():
        Name = (''.join(random.sample(string.ascii_letters + string.digits, 9)))
        JJ += 1
        line = i.strip()
        line = line.upper()
        print(line)
        if line in name:
            print(line)
            exit(-5)
