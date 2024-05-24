import os
import time
import random
import psutil
import argparse
from pywinauto.application import Application
from pywinauto import Desktop

def getProcessIds(process_name):
    res = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            res.append(proc.info['pid'])
    return res

def getRandomStr(length):
    srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choices(srcChar, k=length))

def checkPoint1_1(dlg, filePath):
    # Check point1-1：导入网格
    item = dlg.child_window(title="文件", control_type="TabItem")
    if item.exists():
        item.draw_outline()
        item.click_input(button='left')
    else:
        assert False, f"未找到名称为'文件'的TabItem"

    item = dlg.child_window(title="导入网格", control_type="Button")
    if item.exists():
        item.draw_outline()
        item.click_input(button='left')
    else:
        assert False, f"未找到名称为'导入网格'的Button"

    item = dlg.child_window(title="文件名(N):", control_type="Edit")
    if item.exists():
        item.draw_outline()
        item.type_keys(filePath)
    else:
        assert False, f"未找到名称为'文件名(N):'的Edit"

    item = dlg.child_window(title="打开(O)", control_type="Button")
    if item.exists():
        item.draw_outline()
        item.click_input(button='left')
        time.sleep(5) # 确保网格导入成功
    else:
        assert False, f"未找到名称为'打开(O)'的Button"

def checkPoint1_2(dlg, simulationTreeNodeStart):
    # TODO Check point1-2：网格显示隐藏
    # 现暂未实现显示和隐藏功能
    item = dlg.child_window(auto_id="Global.TreeView", control_type="Tree")
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
        assert False, f"未找到名称为'{chooseTreeNodeName}'的TreeNode"
    else:
        chooseTreeNode.draw_outline()
        chooseTreeNode.click_input(button='left')

    return chooseTreeNode

def checkPoint1_3(dlg):
    # Check point1-3：网格属性变更
    # chooseTreeNode.draw_outline()
    # chooseTreeNode.click_input(button='left')
    item = dlg.child_window(auto_id="WhiteBackground", control_type="Group")
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
        pass
    elif len(chooseAttribute.children()) == 3:
        # print("len(chooseAttribute.children()) == 3")
        # TODO: 由于PowerPi中的控件没有名称，所以暂时无法使用child_window方法获取控件
        pass
    else:
        pass

def checkPoint1_4(dlg):
    # Check point1-4：网格渲染模式及方向变更
    item = dlg.child_window(title="工作台", control_type="TabItem")
    if item.exists():
        item.draw_outline()
        item.click_input(button='left')
    else:
        assert False, f"未找到名称为'工作台'的TabItem"

    # TODO: 完善功能
    # TODO: 使用下面的匹配方式会有多个best match
    # item = dlg.child_window(auto_id="MeshFuncButtonGroup", control_type="Group")

def checkPoint1_5(chooseTreeNode):
    # Check point1-5：网格重命名
    newName = getRandomStr(8)
    chooseTreeNode.draw_outline()
    chooseTreeNode.double_click_input(button='left')
    chooseTreeNode.type_keys("{BACKSPACE}")
    chooseTreeNode.type_keys(newName)
    chooseTreeNode.type_keys("{ENTER}")

def checkPoint1_6(dlg, chooseTreeNode):
    # Check point1-6：网格删除
    chooseTreeNode.click_input(button='right')
    item = dlg.child_window(title="删除", control_type="MenuItem")
    if item.exists():
        item.draw_outline()
        item.click_input(button='left')

def main():
    # 接收参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--powerpipath', type=str, required=False, help='Power-PI的绝对路径', metavar='powerpiPath')
    parser.add_argument('--filepath', type=str, required=True, help='测试用文件的绝对路径', metavar='filePath')
    args = parser.parse_args()

    # Power-Pi路径
    powerpiPath = args.powerpipath

    # 文件路径
    filePath = args.filepath

    # 查询进程ID
    processName = "Power-PI.exe"
    processIds = getProcessIds(processName)
    # print("processIds =", processIds)
    if len(processIds) > 1:
        assert False, f"找到多个名称为'{processName}'的进程"

    apps = Application(backend='uia')
    # windows = Desktop(backend='uia')

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
    dlg = apps['powerpi']

    # 保存若干初态信息
    item = dlg.child_window(auto_id="Global.TreeView", control_type="Tree")
    simulationTreeNodeStart = [child.window_text() for child in item.children()]

    print('测试Check Point1-1')
    # Check point1-1：导入网格
    checkPoint1_1(dlg, filePath)

    print('测试Check Point1-2')
    # Check point1-2：网格显示隐藏
    chooseTreeNode = checkPoint1_2(dlg, simulationTreeNodeStart)

    print('测试Check Point1-3')
    # Check point1-3：网格属性变更
    checkPoint1_3(dlg)

    print('测试Check Point1-4')
    # Check point1-4：网格渲染模式及方向变更
    checkPoint1_4(dlg)

    print('测试Check Point1-5')
    # Check point1-5：网格重命名
    checkPoint1_5(chooseTreeNode)

    print('测试Check Point1-6')
    # Check point1-6：网格删除
    checkPoint1_6(dlg, chooseTreeNode)

    print('测试结束')

if __name__ == '__main__':
    main()
