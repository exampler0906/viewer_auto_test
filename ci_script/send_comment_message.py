# -*- coding: utf-8 -*-
# 将ready to test的消息发送到飞书

import os
import requests
import json
import sys

def main():
    # request标题
    pull_reuqest_url = str(sys.argv[1])

    # 分离出原有pull request id
    pull_request_id = pull_reuqest_url.split("/")[-1]

    # 构造消息json
    json_data = {}
    json_data["msg_type"]= "text" 
    json_data["content"]= { "text": "测试任务:" + pull_request_id + " ready to test" }
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
    print("send message to feishu successfully")

if __name__ == "__main__":
    main()