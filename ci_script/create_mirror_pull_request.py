# -*- coding: utf-8 -*-
# 将viewer仓库的pull request镜像到viewer_auto_test

import sys
import os
import requests
import json
import shutil
from git import Repo

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

def create_or_edit_pull_request(all_open_pull_requests, source_pull_request_number, repository_name, token, viewer_auto_test_token):
    
    check_str = "source pull request:" +  source_pull_request_number
    source_pull_request_description = get_pull_request_description(source_pull_request_number, repository_name, token)
    new_description =  "source pull request:" + source_pull_request_number + "\n" + source_pull_request_description
    is_edit = False
    
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
                    data = {"body": new_description}
                    json_data = json.dumps(data, ensure_ascii=False)

                    # 发送 PATCH 请求以更新 Pull Request 的描述
                    response = requests.patch(url,
                                              headers={
                                              'Authorization': f'Bearer {viewer_auto_test_token}',
                                              'Accept': 'application/vnd.github.v3+json'},
                                              data=json_data.encode('utf-8'))

                    # 检查响应状态码
                    if response.status_code == 200:
                        is_edit = True
                        print(f"pull request {pull_request_number} description updated successfully.")
                    else:
                        print(f"failed to update description for pull request {pull_request_number}.")
                        sys.exit(-1)
        else:
            print(f"failed to fetch pull request description for PR {pull_request_number}")
            continue
    
    # 这种情况说明mirror pull request没有被创建，就创建一个
    if not is_edit:
        url = f"https://api.github.com/repos/exampler0906/viewer_auto_test/pulls"

        # 构建要发送的数据
        data = {
            "title": "测试任务:" + source_pull_request_number,
            "body": new_description,
            "head": source_pull_request_number,
            "base": "master"
        }
        json_data = json.dumps(data, ensure_ascii=False)

        # 发送 POST 请求以创建 Pull Request
        response = requests.post(url,
        headers={
            'Authorization': f'Bearer {viewer_auto_test_token}',
            'Accept': 'application/vnd.github.v3+json'
        },
        data=json_data.encode('utf-8'))

        # 检查响应状态码
        if response.status_code == 201:
            print(f"pull request created successfully")
        else:
            print("failed to create pull request.")
            print("error code:", response.status_code)
            print("error msg:", response.text)


def create_new_branch_in_mirror_repository(source_pull_request_number):
    remote_url = 'https://github.com/exampler0906/viewer_auto_test.git'
    local_path = '../../../../viewer_auto_test/'
    
    if not os.path.exists("../../../../viewer_auto_test"):
        # 不存在的话则拉取对应仓库
        Repo.clone_from(remote_url, local_path)

    # 判断远端是否存在和pull request number相同的分支，若存在说明对应的镜像pull request已经创建
    # 若不存在则创建对应分支并推送至远端
    repo = Repo(local_path)
    remote_branches = [ref.name.split('/')[-1] for ref in repo.remote().refs]
    if source_pull_request_number in remote_branches :
        return
    else:
        # 切换到仓库路径
        os.chdir(local_path)    

        # 放弃本地所有提交
        repo.git.checkout("./")
        repo.git.clean('-df')
        
        # 判断本地分支是否存在
        local_branches = [branch.name for branch in repo.branches]
        if source_pull_request_number in local_branches:
            repo.git.checkout("master")
            repo.git.fetch()
            repo.git.merge("origin/master")
            repo.git.branch('-D', source_pull_request_number)

        # 切换到新分支
        repo.git.checkout(b=source_pull_request_number)

        # 在本地仓库中创建一个新文件
        file_name = 'new_file.txt'
        with open(file_name, 'w') as f:
            f.write("new test task:" + source_pull_request_number)

        # 将新文件添加到 Git 的暂存区
        repo.index.add([file_name])

        # 提交更改到本地仓库
        repo.index.commit('add new file')

        # 推送更改到远程仓库
        origin = repo.remote('origin')
        origin.push(source_pull_request_number)




def main():
    # 原pull request id
    source_pull_request_number = str(sys.argv[1])
    # 原仓库名
    repository_name = str(sys.argv[2])
    # 至少拥有原仓库读权限的token
    token = str(sys.argv[3])
    # 拥有viewer的镜像仓库viewer_auto_test写权限的token
    viewer_auto_test_token = str(sys.argv[4])

    create_new_branch_in_mirror_repository(source_pull_request_number)
    all_open_pull_requests = get_current_pull_request()
    create_or_edit_pull_request(all_open_pull_requests, source_pull_request_number, repository_name, token, viewer_auto_test_token)



if __name__ == "__main__":
    main()



