# -*- coding: utf-8 -*-
# pull request时进行消息转发

import os
import requests
import json
import sys

def main():
    # request标题
    pull_reuqest_url = str(sys.argv[1])
    # comment body
    comment_body = sys.argv[2].encode('utf-16').decode('utf-16')
    print(comment_body)
    # viewer token
    token = str(sys.argv[3])

    # 设置http的请求头
    auth_header = {'Authorization': f'token {token}', 
                   'Accept': 'application/vnd.github.v3+json'}

    # 分离出当前pull request id
    pull_request_id = pull_reuqest_url.split("/")[-1]

    # 获取当前pull request的标题，以获取原有pull request的id
    response = requests.get(f"https://api.github.com/repos/exampler0906/viewer_auto_test/pulls/{pull_request_id}")
    if response.status_code == 200:
        pull_request_data = response.json()
        pull_request_title = pull_request_data['title']
        source_pull_request_id = pull_request_title.split(":")[-1]
    else:
        print("failed to fetch source pull request information.")
        sys.exit(-1)
    source_pull_request_url = "https://github.com/icode-pku/viewer/pull/" + source_pull_request_id

    # 定义 GitHub API 的基础 URL 和认证头部
    base_url = "https://api.github.com"

    # 构造飞书消息体部分
    result =  comment_body + "\n" + source_pull_request_url

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
        sys.exit(-1)
    print("send message successfully.")

    # 如果测试通过，则为原有pull request创建test approve label
    if comment_body == "approve" or comment_body == "Approve":

        # 定义要添加的标签和目标 pull request 的编号
        labels = {}
        labels["labels"] = ["test approve"]

        # 构建 API 请求的 URL
        url = f"{base_url}/repos/icode-pku/viewer/issues/{source_pull_request_id}/labels"

        # 发送 PATCH 请求来给 pull request 添加标签
        response = requests.post(url, headers=auth_header, json=labels)

        # 检查响应是否成功
        if response.status_code == 200:
            print("labels added successfully.")
        else:
            print("failed to add labels.")
            print("status code:", response.status_code)
            print("error message:", response.text)
            sys.exit(-1)

if __name__ == "__main__":
    main()