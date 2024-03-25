# -*- coding: utf-8 -*-
# pull requestʱ������Ϣת��

import os
import requests
import json
import sys

def main():
    # request����
    pull_reuqest_url = str(sys.argv[1])
    # viewer token
    token = str(sys.argv[2])
    auth_header = {'Authorization': f'token {token}', 
                   'Accept': 'application/vnd.github.v3+json'}

    # �����ԭ��pull request id
    pull_request_id = pull_reuqest_url.split("/")[-1]
    source_pull_request_url = "https://github.com/icode-pku/viewer/pull/" + pull_request_id

    # ���� GitHub API �Ļ��� URL ����֤ͷ��
    base_url = "https://api.github.com"

    # ��ȡ���µ�����
    newly_pull_reuqest_comment = ""
    reuqest_url = pull_reuqest_url.replace("pull", "pulls") + "/comments"
    reuqest_url = reuqest_url.replace("https://github.com", base_url + "/repos")
    response = requests.get(reuqest_url, headers=auth_header)
    if response.status_code != 200:
        print("error code:", response.status_code)
        print("error msg:", response.text)
    else:
        print(123)
        print(response.text)
        comments = json.loads(response.text)
        print(comments)
        # ��������ۣ��򷵻���������
        if comments:
            # �������۴���ʱ����������ҵ����µ�����
            latest_comment = max(comments, key=lambda x: x['created_at'])
            newly_pull_reuqest_comment = latest_comment['body']
        else:
            sys.exit(-1)

    # ������Ϣ�岿��
    result =  newly_pull_reuqest_comment + "\n" + source_pull_request_url

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

    # �������ͨ������Ϊԭ��pull request����test approve label
    if newly_pull_reuqest_comment == "approve" or newly_pull_reuqest_comment == "Approve":

        # ����Ҫ��ӵı�ǩ��Ŀ�� pull request �ı��
        labels = ["test_approve"]

        # ���� API ����� URL
        url = f"{base_url}/repos/owner/repository/issues/{pull_request_id}/labels"

        # ���� PATCH �������� pull request ��ӱ�ǩ
        response = requests.post(url, headers=auth_header, json=labels)

        # �����Ӧ�Ƿ�ɹ�
        if response.status_code == 200:
            print("Labels added successfully.")
        else:
            print("Failed to add labels.")
            print("Status code:", response.status_code)
            print("Error message:", response.text)
            sys.exit(-1)

if __name__ == "__main__":
    main()