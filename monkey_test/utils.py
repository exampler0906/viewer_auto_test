import os
import sys
import time
import psutil
import random
from loguru import logger

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
        addLog("ERROR", f"未找到名称为'{title}'的{control_type}")

def getApp(processName:str, powerpiPath:str):
    # 查询进程ID
    processIds = getProcessIds(processName)
    if len(processIds) > 1:
        addLog("ERROR", f"找到多个名称为'{processName}'的进程")
    else:
        pass
    apps = Application(backend='uia')

    if len(processIds) == 1:
        apps.connect(process=processIds[0])
    elif len(processIds) == 0:
        if powerpiPath == None:
            addLog("ERROR", f"请输入Power-PI.exe的绝对路径")
        elif not os.path.exists(powerpiPath):
            addLog("ERROR", f"Power-PI.exe的绝对路径'{powerpiPath}'不存在")
        else:
            apps.start(powerpiPath)
    else:
        pass
    dlg = apps[processName]
    return dlg

def initLog():
    logger.remove()
    log_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    logger.add(sys.stdout, level='TRACE')
    logger.add(f"logs/{log_time}.log", level='TRACE')

def addLog(level:str="INFO", message:str=""):
    if level == "TRACE":
        logger.trace(message)
    elif level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "SUCCESS":
        logger.success(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message + "，程序退出")
        sys.exit(1)
    elif level == "CRITICAL":
        logger.critical(message + "，程序退出")
        sys.exit(1)
    else:
        pass
