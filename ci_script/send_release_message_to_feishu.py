# -*- coding: utf-8 -*-
# pull request时进行消息转发

import os
import requests
import json
import sys

def main():

    # release 页面tag号
    release_tag = str(sys.argv[1])

    # 下载url
    download_url =  f"https://github.com/exampler0906/viewer_release_package/releases/download/{release_tag}/CAE.tar.gz"

    # 构造飞书消息体部分
    result = f"<at user_id=\"all\">所有人</at>\n power_pi最新release包已发布\n 下载连接：{download_url}" 

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
    print("send message to feishu successfully.")

if __name__ == "__main__":
    main()