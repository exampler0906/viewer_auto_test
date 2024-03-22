# -*- coding: utf-8 -*-
# pull request时进行消息转发

import os
import requests
import json
import sys

def main():
    # request标题
    pull_reuqest_title = str(sys.argv[1])
    print(pull_reuqest_title)
    # 最新评论
    newly_pull_reuqest_comment = str(sys.argv[2])
    print(newly_pull_reuqest_comment)
    # viewer token
    token = str(sys.argv[3])
    print(token)

    # 分离出原有pull request id
    pull_request_id = pull_reuqest_title.split(":")[-1]
    source_pull_request_url = "https://github.com/icode-pku/viewer/pull/" + pull_request_id

    # 构造消息体部分
    result = pull_reuqest_title + "\n" + newly_pull_reuqest_comment + "\n" + source_pull_request_url

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

    # 如果测试通过，则为原有pull request创建test approve label
    if newly_pull_reuqest_comment == "approve" or newly_pull_reuqest_comment == "Approve":
        # 定义 GitHub API 的基础 URL 和认证头部
        base_url = "https://api.github.com"
        auth_header = {'Authorization': f'token {token}'}

        # 定义要添加的标签和目标 pull request 的编号
        labels = ["test_approve"]

        # 构建 API 请求的 URL
        url = f"{base_url}/repos/owner/repository/issues/{pull_request_id}/labels"

        # 发送 PATCH 请求来给 pull request 添加标签
        response = requests.post(url, headers=auth_header, json=labels)

        # 检查响应是否成功
        if response.status_code == 200:
            print("Labels added successfully.")
        else:
            print("Failed to add labels.")
            print("Status code:", response.status_code)
            print("Error message:", response.text)

if __name__ == "__main__":
    main()