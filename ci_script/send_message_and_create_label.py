# -*- coding: utf-8 -*-
# pull requestʱ������Ϣת��

import os
import requests
import json
import sys

def main():
    # request����
    pull_reuqest_url = str(sys.argv[1])
    # comment body
    comment_body = str(sys.argv[2])
    # viewer token
    token = str(sys.argv[3])

    # ����http������ͷ
    auth_header = {'Authorization': f'token {token}', 
                   'Accept': 'application/vnd.github.v3+json'}

    # �������ǰpull request id
    pull_request_id = pull_reuqest_url.split("/")[-1]

    # ��ȡ��ǰpull request�ı��⣬�Ի�ȡԭ��pull request��id
    response = requests.get(f"https://api.github.com/repos/exampler0906/viewer_auto_test/pulls/{pull_request_id}")
    if response.status_code == 200:
        pull_request_data = response.json()
        pull_request_title = pull_request_data['title']
        source_pull_request_id = pull_request_title.split(":")[-1]
    else:
        print("failed to fetch source pull request information.")
        sys.exit(-1)
    source_pull_request_url = "https://github.com/icode-pku/viewer/pull/" + source_pull_request_id

    # ���� GitHub API �Ļ��� URL ����֤ͷ��
    base_url = "https://api.github.com"
    
    # ��ȡ�������Ϣ
    # �� JSON �ļ�����ȡ����
    with open('users_list.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        checker_name = data["checker"]["name"]

    # ���������Ϣ�岿��
    result =  comment_body + "\n" + source_pull_request_url + " @" + checker_name

    # ������Ϣjson
    json_data = {}
    json_data["msg_type"]= "text" 
    json_data["content"]= { "text": result }
    json_string = json.dumps(json_data, ensure_ascii=False)

    # ����Ϣͨ��webhook�ķ�ʽת��������
    response = requests.post(
    "https://open.feishu.cn/open-apis/bot/v2/hook/13530db3-8fb8-47be-9456-59aea6699c88",
    headers={'Content-Type': 'application/json'},
    data=json_string.encode('utf-8'))
    
    # �������������ӡ������Ϣ
    if response.status_code != 200:
        print("error code:", response.status_code)
        print("error msg:", response.text)
        sys.exit(-1)
    print("send message successfully.")

    # �������ͨ������Ϊԭ��pull request����test approve label
    if comment_body == "approve" or comment_body == "Approve":

        # ����Ҫ��ӵı�ǩ��Ŀ�� pull request �ı��
        labels = {}
        labels["labels"] = ["test approve"]

        # ���� API ����� URL
        url = f"{base_url}/repos/icode-pku/viewer/issues/{source_pull_request_id}/labels"

        # ���� PATCH �������� pull request ��ӱ�ǩ
        response = requests.post(url, headers=auth_header, json=labels)

        # �����Ӧ�Ƿ�ɹ�
        if response.status_code == 200:
            print("labels added successfully.")
        else:
            print("failed to add labels.")
            print("status code:", response.status_code)
            print("error message:", response.text)
            sys.exit(-1)

if __name__ == "__main__":
    main()