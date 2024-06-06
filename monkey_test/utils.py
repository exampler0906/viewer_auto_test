import os
import psutil
import random

from pywinauto.application import Application

def getProcessIds(process_name:str):
    res = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            res.append(proc.info['pid'])
    return res

def getRandomStr(length:int):
    srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choices(srcChar, k=length))

def getControl(dlg, title:str, control_type:str):
    item = dlg.child_window(title=title, control_type=control_type)
    if item.exists():
        item.draw_outline()
        return item
    else:
        assert False, f"未找到名称为'{title}'的{control_type}"

def getApp(processName:str, powerpiPath:str):
    # 查询进程ID
    processIds = getProcessIds(processName)
    if len(processIds) > 1:
        assert False, f"找到多个名称为'{processName}'的进程"
    else:
        pass
    apps = Application(backend='uia')

    if len(processIds) == 1:
        apps.connect(process=processIds[0])
    elif len(processIds) == 0:
        if powerpiPath == None:
            assert False, f"请输入Power-PI.exe的绝对路径"
        elif not os.path.exists(powerpiPath):
            assert False, f"Power-PI.exe的绝对路径'{powerpiPath}'不存在"
        else:
            apps.start(powerpiPath)
    else:
        pass
    dlg = apps[processName]
    return dlg
