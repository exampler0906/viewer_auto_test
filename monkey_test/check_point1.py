import os
import time
import random
import argparse
from PIL import ImageGrab
from pywinauto.application import Application
from pywinauto import Desktop

from utils import *

def checkPoint1_1(app, filePath):
    # Check point1-1：导入网格
    item = getControl(app, title="文件", control_type="TabItem")
    item.click_input(button='left')

    item = getControl(app, title="导入网格", control_type="Button")
    item.click_input(button='left')

    item = getControl(app, title="文件名(N):", control_type="Edit")
    item.type_keys(filePath)

    item = getControl(app, title="打开(O)", control_type="Button")
    item.click_input(button='left')
    time.sleep(5) # 确保网格导入成功

    # TODO: 使用图像匹配进行校验
    # Check point1-1图像校验
    ckpts1_1_start_time = time.time()
    ckpts1_1_template = cv2.imread('templates/1_importMesh.png')
    ckpts1_1_template = cv2.cvtColor(ckpts1_1_template, cv2.COLOR_RGB2BGR)
    app_rec = app.rectangle()
    bbox = (app_rec.left, app_rec.top, app_rec.right, app_rec.bottom)
    ckpts1_1_target = ImageGrab.grab(bbox)
    ckpts1_1_target = np.array(ckpts1_1_target)

    # print(compareImg(ckpts1_1_template, ckpts1_1_target, mode='mse'),
    #     compareImg(ckpts1_1_template, ckpts1_1_target, mode='ssim'),
    #     compareImg(ckpts1_1_template, ckpts1_1_target, mode='hist'))
    logger.info(f"Check point1-1校验结果: mse={compareImg(ckpts1_1_template, ckpts1_1_target, mode='mse')}, ssim={compareImg(ckpts1_1_template, ckpts1_1_target, mode='ssim')}, hist={compareImg(ckpts1_1_template, ckpts1_1_target, mode='hist')}")
    ckpts1_1_end_time = time.time()
    # print('Check point1-1 time:', ckpts1_1_end_time - ckpts1_1_start_time)

    # plt.figure(figsize=(20, 10))
    # plt.subplot(121)
    # plt.imshow(ckpts1_1_template)
    # plt.subplot(122)
    # plt.imshow(ckpts1_1_target)
    # plt.show()
    logger.info(f"Check point1-1校验时间: {ckpts1_1_end_time - ckpts1_1_start_time}s")

def checkPoint1_2(app, simulationTreeNodeStart):
    # TODO Check point1-2：网格显示隐藏
    # 现暂未实现显示和隐藏功能
    # TODO: 由于PowerPi中的控件没有名称，所以暂时无法使用getControl方法获取控件
    item = app.child_window(auto_id="Global.TreeView", control_type="Tree")
    simulationTreeNodeNow = [child.window_text() for child in item.children()]
    # simulationTreeNodeNow - simulationTreeNodeStart
    simulationTreeNodeDiff = list(set(simulationTreeNodeNow).difference(set(simulationTreeNodeStart)))
    chooseTreeNodeIdx = random.randint(0, len(simulationTreeNodeDiff) - 1)
    chooseTreeNodeName = simulationTreeNodeDiff[chooseTreeNodeIdx]
    chooseTreeNode = None
    for child in item.children():
        if child.window_text() == chooseTreeNodeName:
            chooseTreeNode = child
            break

    if chooseTreeNode == None:
        # addLog("ERROR", f"未找到名称为'{chooseTreeNodeName}'的TreeNode")
        logger.error(f"未找到名称为'{chooseTreeNodeName}'的TreeNode")
    else:
        chooseTreeNode.draw_outline()
        chooseTreeNode.click_input(button='left')

    item = getControl(app, title="文件", control_type="TabItem")
    item.click_input(button='left')

    # TODO: Check point1-2图像校验
    logger.info(f"Check point1-2校验结果: 未实现")

    return chooseTreeNode

def checkPoint1_3(app):
    # Check point1-3：网格属性变更
    # chooseTreeNode.draw_outline()
    # chooseTreeNode.click_input(button='left')
    # TODO: 由于PowerPi中的控件没有名称，所以暂时无法使用getControl方法获取控件
    item = getControl(app, control_type="Group", auto_id="WhiteBackground")
    attributes = []
    for child in item.children():
        if child.friendly_class_name() == "GroupBox":
            attributes.append(child)
    chooseAttributeIdx = random.randint(0, len(attributes) - 1)
    # 测试 固定选中的属性
    # chooseAttributeIdx = 2
    chooseAttribute = attributes[chooseAttributeIdx]
    chooseAttribute.draw_outline()
    if len(chooseAttribute.children()) == 2:
        # print("len(chooseAttribute.children()) == 2")
        # TODO: 由于PowerPi中的控件没有名称，所以暂时无法使用child_window方法获取控件
        # print(chooseAttribute.children())
        # 前半部分为属性名，不可编辑
        itemName = chooseAttribute.children()[0].window_text()
        # print(f"itemName: {itemName}")
        # 后半部分为一组，使用children()[1]获得后半部分
        item = chooseAttribute.children()[1]
        item.draw_outline()
        # 获得并保存后半部分中的两个控件
        editItem = item.children()[0]
        editItem.draw_outline()
        sliderItem = item.children()[1]
        sliderItem.draw_outline()
        # TODO: 应通过滑块获取最大最小值，但是获取的不准确，所以直接写死
        # editMax = sliderItem.max_value()
        # editMin = sliderItem.min_value()
        # print(f"editMin: {editMin}, editMax: {editMax}")
        if itemName == "opacity":
            editMin = 0
            editMax = 1
            is_float = True
        elif itemName == "point_size":
            editMin = 1
            editMax = 50
            is_float = False
        elif itemName == "line_width":
            editMin = 1
            editMax = 50
            is_float = False
        elif itemName == "ambient":
            editMin = 0
            editMax = 1
            is_float = True
        elif itemName == "diffuse":
            editMin = 0
            editMax = 1
            is_float = True
        elif itemName == "specular":
            editMin = 0
            editMax = 1
            is_float = True
        elif itemName == "specular_power":
            editMin = 0
            editMax = 100
            is_float = False
        else:
            pass
        # 获取editItem的值，以便确定输入的退格次数
        editCurValue = editItem.texts()[0]
        # 输入
        editItem.click_input(button='left')
        editItem.type_keys("^a")
        if is_float:
            randomValue = round(random.uniform(editMin, editMax), 2)
        else:
            randomValue = int(random.uniform(editMin, editMax))
        # print(f"randomValue: {randomValue}")
        editItem.type_keys(randomValue)
        item = getControl(app, title="文件", control_type="TabItem")
        item.click_input(button='left')
    elif len(chooseAttribute.children()) == 3:
        # print("len(chooseAttribute.children()) == 3")
        # TODO: 由于PowerPi中的控件没有名称，所以暂时无法使用child_window方法获取控件
        # print(chooseAttribute.children())
        itemName = chooseAttribute.children()[0].window_text()
        # print(f"itemName: {itemName}")
        # print(len(chooseAttribute.chilren()))
        changeColorButton = chooseAttribute.children()[2]
        changeColorButton.draw_outline()
        changeColorButton.click_input(button='left')

        item = getControl(app, title="#ffffff", control_type="Edit")
        item.type_keys("^a")
        randomColor = "#{:06x}".format(random.randint(0, 0xffffff))
        # print(f"randomColor: {randomColor}")
        item.type_keys(randomColor)

        item = getControl(app, title="OK", control_type="Button")
        item.click_input(button='left')
    else:
        pass

    # 复原
    if len(chooseAttribute.children()) == 2:
        editItem.click_input(button='left')
        editItem.type_keys("^a")
        if '.' in str(editCurValue):
            editItem.type_keys(float(editCurValue))
        else:
            editItem.type_keys(int(editCurValue))
    elif len(chooseAttribute.children()) == 3:
        # 这里点击'变更颜色'按钮后，进入选颜色界面，输入框内直接是'#fffffff'，所以可以直接点OK
        changeColorButton.click_input(button='left')
        item = getControl(app, title="OK", control_type="Button")
        item.click_input(button='left')
    else:
        pass
    item = getControl(app, title="文件", control_type="TabItem")
    item.click_input(button='left')

    # Check point1-3：网格属性变更 - 选一个确定的属性变更并验证
    ckpts1_3_attribute = attributes[2]
    ckpts1_3_attribute.draw_outline()

    attributeEditItem = ckpts1_3_attribute.children()[1].children()[0]

    attributeEditItemCurValue = attributeEditItem.texts()[0]

    attributeEditItem.click_input(button='left')
    attributeEditItem.type_keys("^a")
    attributeEditItem.type_keys('50')

    item = getControl(app, title="文件", control_type="TabItem")
    item.click_input(button='left')

    # TODO: Check point1-3图像校验
    ckpts1_3_start_time = time.time()
    ckpts1_3_template = cv2.imread('templates/3_meshAttributeChange.png')
    ckpts1_3_template = cv2.cvtColor(ckpts1_3_template, cv2.COLOR_RGB2BGR)
    app_rec = app.rectangle()
    bbox = (app_rec.left, app_rec.top, app_rec.right, app_rec.bottom)
    ckpts1_3_target = ImageGrab.grab(bbox)
    ckpts1_3_target = np.array(ckpts1_3_target)

    # print(compareImg(ckpts1_3_template, ckpts1_3_target, mode='mse'),
    #     compareImg(ckpts1_3_template, ckpts1_3_target, mode='ssim'),
    #     compareImg(ckpts1_3_template, ckpts1_3_target, mode='hist'))
    logger.info(f"Check point1-3校验结果: mse={compareImg(ckpts1_3_template, ckpts1_3_target, mode='mse')}, ssim={compareImg(ckpts1_3_template, ckpts1_3_target, mode='ssim')}, hist={compareImg(ckpts1_3_template, ckpts1_3_target, mode='hist')}")
    ckpts1_3_end_time = time.time()
    # print('Check point1-3 time:', ckpts1_3_end_time - ckpts1_3_start_time)

    # plt.figure(figsize=(20, 10))
    # plt.subplot(121)
    # plt.imshow(ckpts1_3_template)
    # plt.subplot(122)
    # plt.imshow(ckpts1_3_target)
    # plt.show()
    logger.info(f"Check point1-3校验时间: {ckpts1_3_end_time - ckpts1_3_start_time}s")

    # 复原
    attributeEditItem.click_input(button='left')
    attributeEditItem.type_keys("^a")
    attributeEditItem.type_keys('1')

    item = getControl(app, title="文件", control_type="TabItem")
    item.click_input(button='left')

def checkPoint1_4(app):
    # Check point1-4：网格渲染模式及方向变更
    item = getControl(app, title="工作台", control_type="TabItem")
    item.click_input(button='left')

    # TODO: 完善功能
    # TODO: 在匹配网格渲染模式时，使用下面的匹配方式会有多个best match
    # item = app.child_window(auto_id="MeshFuncButtonGroup", control_type="Group")
    # TODO: 网格渲染模式使用auto_id和control_type匹配时，会有多个best match，故增加一个found_index参数
    # 第一个ComboBox 填充
    item = getControl(app,
                        auto_id="MeshFuncButtonGroup.DirectionSeterWidget",
                        control_type="ComboBox",
                        found_index=0)
    item.click_input(button='left')
    item = getControl(app,
                        title="实色填充",
                        control_type="ListItem")
    item.click_input(button='left')
    # 第二个ComboBox 着色
    item = getControl(app,
                        auto_id="MeshFuncButtonGroup.DirectionSeterWidget",
                        control_type="ComboBox",
                        found_index=1)
    item.click_input(button='left')
    meshColorModeNames = ['表面着色', '线框着色', '表面线框混合着色',
                            '点着色', '片元着色', '图元着色',
                            '顶点着色', '物理着色']
    meshColorModes = []
    for name in meshColorModeNames:
        meshColorMode = getControl(app, title=name, control_type="ListItem", is_draw_outline=False)
        meshColorModes.append((name, meshColorMode))
    chooseMeshColorModeIdx = random.randint(0, len(meshColorModes) - 1)
    chooseMeshColorMode = meshColorModes[chooseMeshColorModeIdx]
    chooseMeshColorMode[1].draw_outline()
    chooseMeshColorMode[1].click_input(button='left')

    ckpts1_4_1_start_time = time.time()
    ckpts1_4_1_template = cv2.imdecode(np.fromfile(f'templates/4_manifold_2Mpa_{chooseMeshColorMode[0]}.png', dtype=np.uint8), cv2.IMREAD_COLOR)
    # ckpts1_4_1_template = cv2.imread(f'templates/4_manifold_2Mpa_{chooseMeshColorMode[0]}.png')
    ckpts1_4_1_template = cv2.cvtColor(ckpts1_4_1_template, cv2.COLOR_RGB2BGR)
    app_rec = app.rectangle()
    bbox = (app_rec.left, app_rec.top, app_rec.right, app_rec.bottom)
    ckpts1_4_1_target = ImageGrab.grab(bbox)
    ckpts1_4_1_target = np.array(ckpts1_4_1_target)

    # print(compareImg(ckpts1_4_1_template, ckpts1_4_1_target, mode='mse'),
    #     compareImg(ckpts1_4_1_template, ckpts1_4_1_target, mode='ssim'),
    #     compareImg(ckpts1_4_1_template, ckpts1_4_1_target, mode='hist'))
    logger.info(f"Check point1-4-1校验结果: mse={compareImg(ckpts1_4_1_template, ckpts1_4_1_target, mode='mse')}, ssim={compareImg(ckpts1_4_1_template, ckpts1_4_1_target, mode='ssim')}, hist={compareImg(ckpts1_4_1_template, ckpts1_4_1_target, mode='hist')}")
    ckpts1_4_1_end_time = time.time()
    # print('Check point1-4-1 time:', ckpts1_4_1_end_time - ckpts1_4_1_start_time)

    # plt.figure(figsize=(20, 10))
    # plt.subplot(121)
    # plt.imshow(ckpts1_4_1_template)
    # plt.subplot(122)
    # plt.imshow(ckpts1_4_1_target)
    # plt.show()
    # print("----------------------------------------------------------------")
    logger.info(f"Check point1-4-1校验时间: {ckpts1_4_1_end_time - ckpts1_4_1_start_time}s")

    # 复原填充
    item = getControl(app,
                        auto_id="MeshFuncButtonGroup.DirectionSeterWidget",
                        control_type="ComboBox",
                        found_index=0)
    item.click_input(button='left')
    item = getControl(app,
                        title="实色填充",
                        control_type="ListItem")
    item.click_input(button='left')

    # 复原着色
    item = getControl(app,
                        auto_id="MeshFuncButtonGroup.DirectionSeterWidget",
                        control_type="ComboBox",
                        found_index=1)
    item.click_input(button='left')
    item = getControl(app,
                        title="线框着色",
                        control_type="ListItem")
    item.click_input(button='left')

    # TODO: 方向变更暂时使用直接获取按钮的方式匹配
    meshDirectChangeNames = ['正x方向', '负x方向',
                                '正y方向', '负y方向',
                                '正z方向', '负z方向',]
    meshDirectChanges = []
    for name in meshDirectChangeNames:
        meshDirectChange = getControl(app, title=name, control_type="Button", is_draw_outline=False)
        meshDirectChanges.append((name, meshDirectChange))
    chooseMeshDirectChangeIdx = random.randint(0, len(meshDirectChanges) - 1)
    chooseMeshDirectChange = meshDirectChanges[chooseMeshDirectChangeIdx]
    chooseMeshDirectChange[1].draw_outline()
    chooseMeshDirectChange[1].click_input(button='left')

    # TODO: 使用图像匹配进行校验
    ckpts1_4_2_start_time = time.time()
    ckpts1_4_2_template = cv2.imdecode(np.fromfile(f'templates/4_manifold_2Mpa_{chooseMeshDirectChange[0]}.png', dtype=np.uint8), cv2.IMREAD_COLOR)
    ckpts1_4_2_template = cv2.cvtColor(ckpts1_4_2_template, cv2.COLOR_RGB2BGR)
    app_rec = app.rectangle()
    bbox = (app_rec.left, app_rec.top, app_rec.right, app_rec.bottom)
    ckpts1_4_2_target = ImageGrab.grab(bbox)
    ckpts1_4_2_target = np.array(ckpts1_4_2_target)

    # print(compareImg(ckpts1_4_2_template, ckpts1_4_2_target, mode='mse'),
    #     compareImg(ckpts1_4_2_template, ckpts1_4_2_target, mode='ssim'),
    #     compareImg(ckpts1_4_2_template, ckpts1_4_2_target, mode='hist'))
    logger.info(f"Check point1-4-2校验结果: mse={compareImg(ckpts1_4_2_template, ckpts1_4_2_target, mode='mse')}, ssim={compareImg(ckpts1_4_2_template, ckpts1_4_2_target, mode='ssim')}, hist={compareImg(ckpts1_4_2_template, ckpts1_4_2_target, mode='hist')}")
    ckpts1_4_2_end_time = time.time()
    # print('Check point1-4-2 time:', ckpts1_4_2_end_time - ckpts1_4_2_start_time)

    # plt.figure(figsize=(20, 10))
    # plt.subplot(121)
    # plt.imshow(ckpts1_4_2_template)
    # plt.subplot(122)
    # plt.imshow(ckpts1_4_2_target)
    # plt.show()
    logger.info(f"Check point1-4-2校验时间: {ckpts1_4_2_end_time - ckpts1_4_2_start_time}s")

    # 复原方向(旋转到正x方向)
    meshDirectChanges[0][1].click_input(button='left')

def checkPoint1_5(app, chooseTreeNode):
    # Check point1-5：网格重命名
    newName = getRandomStr(8)
    chooseTreeNode.draw_outline()
    chooseTreeNode.double_click_input(button='left')
    chooseTreeNode.type_keys(newName)
    chooseTreeNode.type_keys("{ENTER}")

    item = getControl(app, title="工作台", control_type="TabItem")
    item.click_input(button='left')

    # TODO: 使用图像匹配进行校验
    ckpts1_5_start_time = time.time()
    ckpts1_5_template = cv2.imread('templates/5_meshRename.png')
    ckpts1_5_template = cv2.cvtColor(ckpts1_5_template, cv2.COLOR_RGB2BGR)
    app_rec = app.rectangle()
    bbox = (app_rec.left, app_rec.top, app_rec.right, app_rec.bottom)
    ckpts1_5_target = ImageGrab.grab(bbox)
    ckpts1_5_target = np.array(ckpts1_5_target)
    mask_rect = chooseTreeNode.rectangle()
    # 在100缩放下，窗口上边框的高度为23
    ckpts1_5_target[mask_rect.top - 23:mask_rect.bottom - 23,
                    mask_rect.left:mask_rect.right] = 0

    # print(compareImg(ckpts1_5_template, ckpts1_5_target, mode='mse'),
    #     compareImg(ckpts1_5_template, ckpts1_5_target, mode='ssim'),
    #     compareImg(ckpts1_5_template, ckpts1_5_target, mode='hist'))
    logger.info(f"Check point1-5校验结果: mse={compareImg(ckpts1_5_template, ckpts1_5_target, mode='mse')}, ssim={compareImg(ckpts1_5_template, ckpts1_5_target, mode='ssim')}, hist={compareImg(ckpts1_5_template, ckpts1_5_target, mode='hist')}")
    ckpts1_5_end_time = time.time()
    # print('Check point1-5 time:', ckpts1_5_end_time - ckpts1_5_start_time)

    # plt.figure(figsize=(20, 10))
    # plt.subplot(121)
    # plt.imshow(ckpts1_5_template)
    # plt.subplot(122)
    # plt.imshow(ckpts1_5_target)
    # plt.show()
    logger.info(f"Check point1-5校验时间: {ckpts1_5_end_time - ckpts1_5_start_time}s")

def checkPoint1_6(app, chooseTreeNode):
    # Check point1-6：网格删除
    chooseTreeNode.click_input(button='right')
    item = getControl(app, title="删除", control_type="MenuItem")
    if item.exists():
        item.draw_outline()
        item.click_input(button='left')
    item = getControl(app, title="工作台", control_type="TabItem")
    item.click_input(button='left')

    # TODO: 使用图像匹配进行校验
    chpts1_6_start_time = time.time()
    chpts1_6_template = cv2.imread('templates/6_meshDelete.png')
    chpts1_6_template = cv2.cvtColor(chpts1_6_template, cv2.COLOR_RGB2BGR)
    app_rec = app.rectangle()
    bbox = (app_rec.left, app_rec.top, app_rec.right, app_rec.bottom)
    chpts1_6_target = ImageGrab.grab(bbox)
    chpts1_6_target = np.array(chpts1_6_target)

    # print(compareImg(chpts1_6_template, chpts1_6_target, mode='mse'),
    #     compareImg(chpts1_6_template, chpts1_6_target, mode='ssim'),
    #     compareImg(chpts1_6_template, chpts1_6_target, mode='hist'))
    logger.info(f"Check point1-6校验结果: mse={compareImg(chpts1_6_template, chpts1_6_target, mode='mse')}, ssim={compareImg(chpts1_6_template, chpts1_6_target, mode='ssim')}, hist={compareImg(chpts1_6_template, chpts1_6_target, mode='hist')}")
    chpts1_6_end_time = time.time()
    # print('Check point1-6 time:', chpts1_6_end_time - chpts1_6_start_time)

    # plt.figure(figsize=(20, 10))
    # plt.subplot(121)
    # plt.imshow(chpts1_6_template)
    # plt.subplot(122)
    # plt.imshow(chpts1_6_target)
    # plt.show()
    logger.info(f"Check point1-6校验时间: {chpts1_6_end_time - chpts1_6_start_time}s")

def main():
    # 初始化日志模块
    initLog()

    # 接收参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--powerpipath', type=str, required=False, help='Power-PI的绝对路径', metavar='powerpiPath')
    parser.add_argument('--filepath', type=str, required=True, help='测试用文件的绝对路径', metavar='filePath')
    args = parser.parse_args()

    # Power-Pi路径
    powerpiPath = args.powerpipath
    # addLog("INFO", f"Power-PI的绝对路径为：{powerpiPath}")
    logger.info(f"Power-PI的绝对路径为: {powerpiPath}")

    # 文件路径
    filePath = args.filepath
    # addLog("INFO", f"测试用文件的绝对路径为：{filePath}")
    logger.info(f"测试用文件的绝对路径为: {filePath}")

    processName = "Power-PI.exe"
    app = getApp(processName=processName, powerpiPath=powerpiPath)
    # TODO: 使用图像匹配进行校验
    # addLog("INFO", f"成功连接Power-PI")
    logger.info(f"成功连接Power-PI")

    # 保存若干初态信息
    item = app.child_window(auto_id="Global.TreeView", control_type="Tree")
    simulationTreeNodeStart = [child.window_text() for child in item.children()]

    # 启动时图像校验
    app_start_start_time = time.time()
    app_start_template = cv2.imread('templates/0_start.png')
    app_start_template = cv2.cvtColor(app_start_template, cv2.COLOR_RGB2BGR)
    app_rec = app.rectangle()
    bbox = (app_rec.left, app_rec.top, app_rec.right, app_rec.bottom)
    app_start_target = ImageGrab.grab(bbox)
    app_start_target = np.array(app_start_target)

    print(compareImg(app_start_template, app_start_target, mode='mse'),
        compareImg(app_start_template, app_start_target, mode='ssim'),
        compareImg(app_start_template, app_start_target, mode='hist'))
    app_start_end_time = time.time()
    # print(f"app start time: {app_start_end_time - app_start_start_time}")

    # plt.figure(figsize=(20, 10))
    # plt.subplot(121)
    # plt.imshow(app_start_template)
    # plt.subplot(122)
    # plt.imshow(app_start_target)
    # plt.show()
    logger.info(f"App启动成功")
    logger.info(f"App启动校验时间{app_start_end_time - app_start_start_time}")

    # addLog("INFO", "测试Check Point1-1")
    logger.info("测试Check Point1-1")
    # Check point1-1：导入网格
    checkPoint1_1(app, filePath)

    # addLog("INFO", "测试Check Point1-2")
    logger.info("测试Check Point1-2")
    # Check point1-2：网格显示隐藏
    chooseTreeNode = checkPoint1_2(app, simulationTreeNodeStart)

    # addLog("INFO", "测试Check Point1-3")
    logger.info("测试Check Point1-3")
    # Check point1-3：网格属性变更
    checkPoint1_3(app)

    # addLog("INFO", "测试Check Point1-4")
    logger.info("测试Check Point1-4")
    # Check point1-4：网格渲染模式及方向变更
    checkPoint1_4(app)

    # addLog("INFO", "测试Check Point1-5")
    logger.info("测试Check Point1-5")
    # Check point1-5：网格重命名
    checkPoint1_5(app, chooseTreeNode)

    # addLog("INFO", "测试Check Point1-6")
    logger.info("测试Check Point1-6")
    # Check point1-6：网格删除
    checkPoint1_6(app, chooseTreeNode)

    # addLog("INFO", "测试结束")
    logger.info("测试结束")

if __name__ == '__main__':
    main()
