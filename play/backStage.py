import requests,copy
from logAnalysisUtil import *
def get_parameters(response,paths):
    path_list = paths.split('/')
    parameters = copy.deepcopy(response)
    for path in path_list:
        if path != '#':
            parameters = parameters.get(path)
    properties = parameters.get('properties')
    parameters = list(properties.keys())
    return parameters
def get_api():
    url = 'http://192.168.10.211:8084/v3/api-docs'
    response = requests.get(url)
    response = response.json()
    paths = response.get('paths')
    api_list = []
    for url_path,value in paths.items():
        parameters_type = 1
        print(url_path,value)
        try:
            url_post = value.get('post')
            if 'parameters' in url_post.keys():
                url_parameters = url_post.get('parameters')
                print('parameters')
            else:
                requestBody = url_post.get('requestBody')
                _content = requestBody.get('content')
                for _content_type,ref_path in _content.items():
                    if '$ref' in ref_path.get('schema'):
                        ref_url = ref_path.get('schema').get('$ref')
                        print('$ref')
                    else:
                        ref_url = ref_path.get('schema').get('items').get('$ref')
                        parameters_type = 2
                        print('items')
                    parameters = get_parameters(response,ref_url)
        except:
            print("else")
        api_list.append((url_path,parameters_type))
    return api_list
def loginBackStage(session):
    loginUrl = 'http://192.168.10.211:8080/login'
    data = {'username':'Y001','password':'111'}
    response = session.post(url = loginUrl,data = data)
    response = response.json()
    if response.get('status',0) == 200:
        return response.get('token','')
def getBackStageGameReport(session,token,startTime, endTime,urlType,api_url):
    api = api_url[0]
    parameters_type = api_url[1]
    if parameters_type == 2:
        data = '1000'
    else:
        startDay = startTime.split(' ')[0]
        endDay = startTime.split(' ')[0]
        data = {"cid": "",
                "dateMax": endDay,
                "dateMin": startDay,
                "gameType": "",
                "gid": "",
                "limit": 10,
                "page": 1,
                "style": ""}
        data = json.dumps(data)
    url = 'http://192.168.10.211:8080' + api
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'token':token}
    response = session.post(url = url,data = data,headers = headers)
    try:
        response = response.json()
    except:
        pass
    return response
#     if response.get('code','') == '0':
#         return response.get('data','')
def init_requests():
    session = requests.session()
    return session
session = init_requests()
# token = loginBackStage(session)
startTime = "2021-12-28 00:00:00"
endTime = "2021-12-29 00:00:00"
api_url_list = get_api()
for api_url in api_url_list:
    print(api_url)
    token = loginBackStage(session)
    for i in range(101):
        response = getBackStageGameReport(session,token,startTime, endTime,1,api_url)
        # print(response)
        try:
            if i == 100 and response.get('status') != 500:
                    print(api_url,response)
                    with open('error_api.log','a') as f:
                        f.write(api_url[0] + ' ' + str(response) + '\n')
        except:
            with open('error_api.log', 'a') as f:
                f.write(api_url[0] + ' ' + str(response) + '\n')



