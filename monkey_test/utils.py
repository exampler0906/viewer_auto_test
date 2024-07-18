import os
import cv2
import sys
import time
import math
import psutil
import random
import ctypes
import numpy as np
from loguru import logger

from pywinauto.application import Application
from skimage.metrics import structural_similarity as ssim

def getProcessIds(process_name:str):
    res = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            res.append(proc.info['pid'])
    return res

def getRandomStr(length:int):
    srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choices(srcChar, k=length))

def getControl(app, **kwargs):
    """获取app的控件

    Args:
        app (_type_): _description_
        title (str): _description_
        control_type (str): _description_
        auto_id (str): _description_
        found_index (int): _description_
        is_draw_outline (bool): _description_
    """
    title = kwargs.get("title", None)
    control_type = kwargs.get("control_type", None)
    auto_id = kwargs.get("auto_id", None)
    found_index = kwargs.get("found_index", 0)
    is_draw_outline = kwargs.get("is_draw_outline", True)

    item = app.child_window(title=title,
                            control_type=control_type,
                            auto_id=auto_id,
                            found_index=found_index)
    if item.exists():
        if is_draw_outline:
            item.draw_outline()
        else:
            pass
        return item
    else:
        # addLog("ERROR", f"未找到名称为'{title}'的{control_type}")
        logger.error(f"未找到名称为'{title}'的{control_type}")

def getApp(processName:str, powerpiPath:str):
    # 查询进程ID
    processIds = getProcessIds(processName)
    if len(processIds) > 1:
        # addLog("ERROR", f"找到多个名称为'{processName}'的进程")
        logger.error(f"找到多个名称为'{processName}'的进程")
    else:
        pass
    apps = Application(backend='uia')

    if len(processIds) == 1:
        apps.connect(process=processIds[0])
    elif len(processIds) == 0:
        if powerpiPath == '':
            # addLog("ERROR", f"请输入Power-PI.exe的绝对路径")
            logger.error(f"请输入Power-PI.exe的绝对路径")
        elif not os.path.exists(powerpiPath):
            # addLog("ERROR", f"Power-PI.exe的绝对路径'{powerpiPath}'不存在")
            logger.error(f"Power-PI.exe的绝对路径'{powerpiPath}'不存在")
        else:
            apps.start(powerpiPath)
    else:
        pass
    app = apps[processName]
    return app

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

def getScreenScalingFactor():
    # 获取设备上下文
    hdc = ctypes.windll.user32.GetDC(0)
    # 获取DPI(Dots Per Inch)
    dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88是LOGPIXELSX的常量值
    # 释放设备上下文
    ctypes.windll.user32.ReleaseDC(0, hdc)
    # 计算缩放比
    scalingFactor = dpi / 96.0  # 96DPI是100%缩放比
    return scalingFactor

def compareImg(template:np.ndarray, target:np.ndarray, mode:str="mse"):
    if template.shape != target.shape:
        # addLog("INFO", "模板和目标的大小不一致")
        logger.info(f"模板和目标的大小不一致，模板大小：{template.shape}，目标大小：{target.shape}")
        heightDiff = abs(template.shape[0] - target.shape[0])
        # 根据heightDiff的值在target图片的底部进行填充
        target = cv2.copyMakeBorder(target, 0, heightDiff, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    if mode == "mse":
        mse = np.sum((template.astype("float") - target.astype("float")) ** 2)
        mse /= float(template.shape[0] * template.shape[1])
        return mse
    elif mode == "ssim":
        ssim_value, diff = ssim(template, target, full=True, multichannel=True, channel_axis=2)
        return ssim_value
    elif mode == "hist":
        hist_template = cv2.calcHist([template], [0], None, [256], [0, 256])
        hist_target = cv2.calcHist([target], [0], None, [256], [0, 256])
        cv2.normalize(hist_template, hist_template)
        cv2.normalize(hist_target, hist_target)
        comparison = cv2.compareHist(hist_template, hist_target, cv2.HISTCMP_CORREL)
        return comparison
    elif mode == "match":
        pass
    else:
        pass
