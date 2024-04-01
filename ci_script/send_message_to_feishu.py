# -*- coding: utf-8 -*-
# pull request时进行消息转发

import os
import requests
import json
import sys

def get_pull_request_description(pull_request_number, repository_name, token):
    # 构建 GitHub REST API 请求 URL
    api_url = f"https://api.github.com/repos/"+ repository_name + "/pulls/" + pull_request_number

    # 发送 HTTP GET 请求获取拉取请求信息
    response = requests.get(
        api_url,
        headers={
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )

    # 如果请求成功，则返回拉取请求的描述，否则返回 None
    if response.ok:
        return response.json().get('body')
    else:
        print("error code:", response.status_code)
        print("error msg:", response.text)
        return None

def main():
    # 原pull request id
    pull_request_number = str(sys.argv[1])
    # 原仓库名
    repository_name = str(sys.argv[2])
    # 至少拥有原仓库读权限的token
    token = str(sys.argv[3])

    result = get_pull_request_description(pull_request_number, repository_name, token)
    if result == None:
        sys.exit(-1)

    # 构造消息json
    json_data = {}
    json_data["msg_type"]= "text" 
    json_data["content"]= { "text": result }
    json_string = json.dumps(json_data, ensure_ascii=False)

    # 将消息通过webhook的方式转发到飞书
    response = requests.post(
    "https://open.feishu.cn/open-apis/bot/v2/hook/13530db3-8fb8-47be-9456-59aea6699c88",
    headers={'Content-Type': 'application/json'},
    data=json_string.encode('utf-8'))
    
    # 如果请求错误则打印错误信息
    if response.status_code != 200:
        print("error code:", response.status_code)
        print("error msg:", response.text)
    else:
        print("send message to feishu successfully")

if __name__ == "__main__":
    main()
