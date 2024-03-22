# -*- coding: utf-8 -*-
# pull requestʱ������Ϣת��

import os
import requests
import json
import sys

def main():
    # request����
    pull_reuqest_title = str(sys.argv[1])
    print(pull_reuqest_title)
    # ��������
    newly_pull_reuqest_comment = str(sys.argv[2])
    print(newly_pull_reuqest_comment)
    # viewer token
    token = str(sys.argv[3])
    print(token)

    # �����ԭ��pull request id
    pull_request_id = pull_reuqest_title.split(":")[-1]
    source_pull_request_url = "https://github.com/icode-pku/viewer/pull/" + pull_request_id

    # ������Ϣ�岿��
    result = pull_reuqest_title + "\n" + newly_pull_reuqest_comment + "\n" + source_pull_request_url

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

    # �������ͨ������Ϊԭ��pull request����test approve label
    if newly_pull_reuqest_comment == "approve" or newly_pull_reuqest_comment == "Approve":
        # ���� GitHub API �Ļ��� URL ����֤ͷ��
        base_url = "https://api.github.com"
        auth_header = {'Authorization': f'token {token}'}

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

if __name__ == "__main__":
    main()