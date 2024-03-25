# -*- coding: utf-8 -*-
# pull request时进行消息转发

import os
import requests
import json
import sys

def main():
	comment_body = sys.argv[1].encode('utf-8').decode('utf-8')
	print(comment_body)

if __name__ == "__main__":
    main()