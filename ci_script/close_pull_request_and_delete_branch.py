# -*- coding: utf-8 -*-
# 将viewer仓库的pull request镜像到viewer_auto_test

import sys
import os
import requests
import json
import shutil
from git import Repo

def get_current_pull_request():
	 # 构建 GitHub REST API 请求 URL
    url = f"https://api.github.com/repos/exampler0906/viewer_auto_test/pulls"

    # 发送 GET 请求获取所有 pull request
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应内容并筛选出所有 open 状态的 pull request 的 ID
        open_pull_requests = [pull_request['number'] for pull_request in response.json() if pull_request['state'] == 'open']
        return open_pull_requests
    else:
        print("failed to fetch pull requests")
        print("error code:", response.status_code)
        print("error msg:", response.text)
        return []


def close_pull_request(source_pull_request_number, viewer_auto_test_token):
    check_str = "source pull request:" +  source_pull_request_number
    all_open_pull_requests = get_current_pull_request()
    
    for pull_request_number in all_open_pull_requests:
        # 获取当前各个open状态的pull request描述
        url = f"https://api.github.com/repos/exampler0906/viewer_auto_test/pulls/{pull_request_number}"

        # 发送 GET 请求获取指定 pull request 的信息
        response = requests.get(url)

        # 检查响应状态码
        if response.status_code == 200:
            # 返回 pull request 的描述
            description = response.json().get('body')
            if not description == None:
                if check_str in description:
                
                    # 构建要发送的数据
                    data = {"state": "closed"}
                    json_data = json.dumps(data, ensure_ascii=False)

                    # 发送 PATCH 请求以关闭 Pull Request
                    response = requests.patch(url,
                                              headers={
                                              'Authorization': f'Bearer {viewer_auto_test_token}',
                                              'Accept': 'application/vnd.github.v3+json'},
                                              data=json_data.encode('utf-8'))

                    # 检查响应状态码
                    if response.status_code == 200:
                        print(f"pull request {pull_request_number} close successfully.")
                    else:
                        print(f"failed to close pull request {pull_request_number}.")
                        sys.exit(-1)
        else:
            print(f"failed to fetch pull request description for PR {pull_request_number}")
            continue


def delete_branch(source_pull_request_number, viewer_auto_test_token):
    url = f"https://api.github.com/repos/exampler0906/viewer_auto_test/git/refs/{source_pull_request_number}"

    # 删除对应分支
    response = requests.delete(url,
                                headers={
                                'Authorization': f'Bearer {viewer_auto_test_token}',
                                'Accept': 'application/vnd.github.v3+json'})

    # 检查响应状态码
    if response.status_code == 204:
        print(f"delete branch {source_pull_request_number} successfully.")
    else:
        print(f"failed to delete branch {source_pull_request_number}.")
        sys.exit(-1)

def main():
    # 原pull request id
    source_pull_request_number = str(sys.argv[1])
    # 拥有viewer的镜像仓库viewer_auto_test写权限的token
    viewer_auto_test_token = str(sys.argv[2])

    # 关闭镜像pull request
    close_pull_request(source_pull_request_number, viewer_auto_test_token)

    # 删除镜像pull request对应的branch
    delete_branch(source_pull_request_number, viewer_auto_test_token)
   

if __name__ == "__main__":
    main()
