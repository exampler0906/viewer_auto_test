# monkey_test脚本说明

## 环境准备
- windows环境
- python3 (version > 3.10)
- pywinauto

## pywinauto安装
~~~
pip install pywinauto
~~~

## monkey_test基本介绍
- monkey_test模拟的是用户针对软件的随机操作，旨在验证软件运行的稳定性。
- monkey_test的测试一共有三组，分别用于测试初始状态、网格和配置文件导入后的状态、网格配置文件及后处理文件导入后的状态。
- monkey_test的每组测试的数量由启动参数指定。

## monkey_test脚本使用示例
~~~
python .\run_gui_test.py ..\..\viewer\build\Release\Power-PI.exe[ application path ] 1 [each test group test times]
~~~
