# -*- coding: utf-8 -*-

import time
import random
import threading
import sys
import os
import subprocess
from PIL import ImageGrab
from datetime import datetime
from pywinauto import timings
from pywinauto.timings import Timings
from pywinauto import controls
from pywinauto.application import Application
from pywinauto.timings import always_wait_until_passes
from pywinauto.controls.common_controls import UpDownWrapper

# 等待页面初始化完成的时间为10s
Timings.window_find_timeout = 10

def execute_application(execute_application):
    app = Application(backend="uia").start(execute_application)

    time.sleep(10)
    cmd = ["procdump.exe","-e","-ma", "-g", "Power-PI.exe"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return app

def get_current_top_dialog_controls(app):

    window = app.top_window()
    window.wait('ready')

    # 文件相关弹窗不用测试
    button = window.child_window(title="取消", control_type="Button")
    if button.exists():
        button.click_input(button='left')
        window = app.top_window()
        window.wait('ready')

    # 控件栈
    wrapper_stack = [window]

    # 控件队列
    control_vector = []

    # 遍历每个控件并输出其控件名和类名
    while wrapper_stack:
        top_item = wrapper_stack.pop()
        top_item_children = top_item.children()
        # 只提取最基础的元素
        if len(top_item_children) == 0: 
            # 最底层的容器控件，或者没有交互意义的控件一概不处理
            if (top_item.friendly_class_name() != "Static" and 
                top_item.friendly_class_name() != "GroupBox" and 
                top_item.friendly_class_name() != "Thumb" and
                top_item.friendly_class_name() != "Image" and
                len(top_item.texts()) > 0 and
                top_item.texts()[0] != "Power-PI"):
                control_vector.append(top_item)
                #print(top_item.get_properties())

        for child in top_item_children:
            # 排除WIN应用自带的最大化，窗口化，最小化，关闭的等按钮, 此种过滤方式只是临时方案
            if ((child.friendly_class_name() == "Button" and len(child.texts()) != 0 and child.parent().friendly_class_name() == "TitleBar")  or
            (child.friendly_class_name() == "MenuItem" and child.texts()[0] == u"系统")):
                continue
            wrapper_stack.append(child)

    return control_vector

"""
def get_a_random_control(app):
    print(datetime.datetime.now())
    window = app.top_window()
    window.wait('ready')

    # 控件队列
    control_vector = []

    # 控件栈
    print(datetime.datetime.now())
    while not control_vector:
        window_children = window.children()
        a_random_control = window_children[random.randint(0,len(window_children)-1)]
        
         # 排除WIN应用自带的最大化，窗口化，最小化，关闭的等按钮
        if a_random_control.friendly_class_name() == "TitleBar" :
            continue;

        wrapper_stack = [a_random_control]

        # 遍历每个控件并输出其控件名和类名
        
        while wrapper_stack:
            control = wrapper_stack.pop()
            
            control_children = control.children()
            
            # 只提取最基础的元素
            if len(control_children) == 0: 
                # 没有实际含义的控件，最底层的容器控件一概不处理
                if (control.friendly_class_name() != "Static" and 
                    control.friendly_class_name() != "GroupBox" and 
                    control.class_name() != "Thumb"):
                    control_text = control.texts()
                    # 不知道具体含义的控件一概不处理
                    if not (len(control_text) == 1 and control_text[0] == ''):
                        control_vector.append(control)

            for child in control_children:
                ## 排除WIN应用自带的最大化，窗口化，最小化，关闭的等按钮, 此种过滤方式只是临时方案
                #if child.friendly_class_name() == "Button" and len(child.texts()) != 0 and child.parent().friendly_class_name() == "TitleBar":
                    #continue
                wrapper_stack.append(child)
    

    return control_vector[random.randint(0,len(control_vector)-1)]
"""

def generate_code():
    str_pattern='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
    string = ''

    # 随机长度，不超过20个字符
    length = random.randint(1,20)
    for _ in range(0,length):
        string = string+str_pattern[random.randint(0,len(str_pattern)-1)]

    return string


def random_button_action(control, log_file):
    
    # 目前先提升主要操作的执行效率
    action_type = random.randint(0,1)
    if action_type == 0:
        control.click_input(button='left')
        print("left click button")
        log_file.write("left click button\n")
    elif action_type == 1:
        control.double_click_input(button='left')
        print("left double click button")
        log_file.write("left double click button\n")

    """
    # 随机执行，左键单击，左键双击，右键单价，右键双击这几种操作
    action_type = random.randint(0,3)

    if action_type == 0:
        control.click_input(button='left')
        print("left click button")
        log_file.write("left click button\n")
    elif action_type == 1:
        control.double_click_input(button='left')
        print("left double click button")
        log_file.write("left double click button\n")
    elif action_type == 2:
        control.click_input(button='right')
        print("right click button")
        log_file.write("right click button\n")
    elif action_type == 3:
        control.double_click_input(button='right')
        print("right double click button")
        log_file.write("right double click button\n")
    """

def random_combobox_action(control, log_file):
    
    # 目前先提升主要操作的执行效率
    grandparent = control.parent().parent()
    # 焦点切换是必须的
    grandparent.click_input(button='left')
    grandparent.type_keys("%{DOWN}")
    control.click_input(button='left')
    print("select a combobox item")
    log_file.write("select a combobox item\n")

    """
    # 随机执行，左键单击，左键双击，右键单价，右键双击，下拉选择框并选择其中的按钮
    action_type = random.randint(0,4)
    grandparent = control.parent().parent()

    if action_type == 0:
        grandparent.click_input(button='left')
        print("left click combobox")
        log_file.write("left click combobox\n")
    elif action_type == 1:
        grandparent.double_click_input(button='left')
        print("left double click combobox")
        log_file.write("left double click combobox\n")
    elif action_type == 2:
        grandparent.click_input(button='right')
        print("right click combobox")
        log_file.write("right click combobox\n")
    elif action_type == 3:
        grandparent.double_click_input(button='right')
        print("right double click combobox")
        log_file.write("right double click combobox\n")
    elif action_type == 4:
        grandparent.type_keys("%{DOWN}")
        control.click_input(button='left')
        print("select a combobox item")
        log_file.write("select a combobox item\n")
    """


def random_tab_action(control, log_file):
    
    # 目前先提升主要操作的执行效率
    action_type = random.randint(0,1)
    if action_type == 0:
        control.click_input(button='left')
        print("left click tab item")
        log_file.write("left click tab item\n")
    elif action_type == 1:
        control.double_click_input(button='left')
        print("left double click tab item")
        log_file.write("left double click tab item\n")

    """
    # 随机执行，左键单击，左键双击，右键单价，右键双击这几种操作
    action_type = random.randint(0,3)

    if action_type == 0:
        control.click_input(button='left')
        print("left click tab item")
        log_file.write("left click tab item\n")
    elif action_type == 1:
        control.double_click_input(button='left')
        print("left double click tab item")
        log_file.write("left double click tab item\n")
    elif action_type == 2:
        control.click_input(button='right')
        print("right click tab item")
        log_file.write("right click tab item\n")
    elif action_type == 3:
        control.double_click_input(button='right')
        print("right double click tab item")
        log_file.write("right double click tab item\n")
    """

def random_tree_action(control, log_file):
    
    # 目前先提升主要操作的执行效率
    action_type = random.randint(0,1)
    if action_type == 0:
        control.click_input(button='right')
        print("left click tree item")
        log_file.write("left click tree item\n")
    elif action_type == 1:
        control.click_input(button='right')
        print("right click tree item")
        log_file.write("right click tree item\n")

    # 改变当前节点的状态，保证所有的节点都有机会被测试到
    control.double_click_input(button='left')

    # 尝试切换滑动条的位置，当存在滑动条时，不可见的位置无法访问
    tree = control.parent()
    # 向上或向下移动滑动条
    wheel_type = random.randint(0,1)
    if wheel_type == 0:
        # 向上
        tree.wheel_mouse_input(wheel_dist = 1)
    else:
        # 向下
        tree.wheel_mouse_input(wheel_dist = -1)

    """
    # 随机执行，左键单击，左键双击，右键单价，右键双击这几种操作
    action_type = random.randint(0,3)

    if action_type == 0:
        control.click_input(button='left')
        print("left click tree item")
        log_file.write("left click tree item\n")
    elif action_type == 1:
        control.double_click_input(button='left')
        print("left double click tree item")
        log_file.write("left double click tree item\n")
    elif action_type == 2:
        control.click_input(button='right')
        print("right click tree item")
        log_file.write("right click tree item\n")
    elif action_type == 3:
        control.double_click_input(button='right')
        print("right double click tree item")
        log_file.write("right double click tree item\n")
    """
    
def random_menu_action(control, log_file):
    # 目前先提升主要操作的执行效率

    action_type = random.randint(0,1)
    if action_type == 0:
        control.click_input(button='right')
        print("left click menu item")
        log_file.write("left click menu item\n")
    elif action_type == 1:
        control.click_input(button='right')
        print("right click menu item")
        log_file.write("right click menu item\n")

    """
    # 随机执行，左键单击，左键双击，右键单价，右键双击这几种操作
    action_type = random.randint(0,3)

    if action_type == 0:
        control.click_input(button='left')
        print("left click tab item")
        log_file.write("left click tab item\n")
    elif action_type == 1:
        control.double_click_input(button='left')
        print("left double click tab item")
        log_file.write("left double click tab item\n")
    elif action_type == 2:
        control.click_input(button='right')
        print("right click tab item")
        log_file.write("right click tab item\n")
    elif action_type == 3:
        control.double_click_input(button='right')
        print("right double click tab item")
        log_file.write("right double click tab item\n")
    """
    
def random_radiobutton_action(control, log_file):
    # 目前先提升主要操作的执行效率

    control.click_input(button='left')
    print("click radio button")
    log_file.write("click radio button\n")


def random_checkbox_action(control, log_file):
    # 目前先提升主要操作的执行效率

    control.click_input(button='left')
    print("click check box")
    log_file.write("click check box\n")


def random_edit_action(control, log_file):
    # 目前先提升主要操作的执行效率

    control.set_edit_text(generate_code())
    print("input into edit")
    log_file.write("input into edit\n")


def random_slider_action(control, log_file):
    # 目前先提升主要操作的执行效率

    max_value = control.max_value()
    min_value = control.min_value()
    control.set_value(random.randint(min_value, max_value))
    print("set slider")
    log_file.write("set slider\n")

def random_updown_action(control, log_file):
    # 目前先提升主要操作的执行效率
    # updown 目前暂时不支持
    print("updown not support now")
    log_file.write("updown not support now\n")

def execute_a_action(controls, log_file):
    random_number = random.randint(0,len(controls)-1)
    control = controls[random_number]
    #print(control.friendly_class_name())

    log_file.write(str(control.get_properties()) + '\n')
    if control.friendly_class_name() == "Button" and control.is_enabled():
        random_button_action(control, log_file)
    elif control.friendly_class_name() == "ListItem" and control.is_enabled():
        random_combobox_action(control, log_file)
    elif control.friendly_class_name() == "TabItem" and control.is_enabled():
        random_tab_action(control, log_file)
    elif control.friendly_class_name() == "TreeItem" and control.is_enabled():
        random_tree_action(control, log_file)
    elif control.friendly_class_name() == "RadioButton" and control.is_enabled():
        random_radiobutton_action(control, log_file)
    elif control.friendly_class_name() == "CheckBox" and control.is_enabled():
        random_checkbox_action(control, log_file)
    elif control.friendly_class_name() == "Edit" and control.is_enabled() and control.is_editable():
        random_edit_action(control, log_file)
    elif control.friendly_class_name() == "Slider" and control.is_enabled():
        random_slider_action(control, log_file)
    # QDoubleSpinBox/QSpinBox 暂时不支持
    elif control.friendly_class_name() == "UpDown" and control.is_enabled():
        random_updown_action(control, log_file)
    elif control.friendly_class_name() == "MenuItem" and control.is_enabled():
        random_menu_action(control, log_file)
 
    


def compare_controls(old_controls, new_controls):
        if len(old_controls) != len(new_controls):
            return False

        index = 0
        while index < len(old_controls):
            if (old_controls[index].texts() != new_controls[index].texts() or
            old_controls[index].class_name() != new_controls[index].class_name() or
            old_controls[index].friendly_class_name() != new_controls[index].friendly_class_name()):
                return False    
            index += 1
        return True


#@always_wait_until_passes(0.5,0.5)
def monkey_test(app, log_file):
    
    # 目前先不做每个异常作详细的异常处理，遇到异常就整体退出
    #start_time = time.time()
    controls = get_current_top_dialog_controls(app)
    execute_a_action(controls, log_file)
    #end_time = time.time()
    #print(end_time - start_time)

    if not app.top_window().is_visible():
        kill_application(app, log_file)

    """
    try :
        controls = get_current_top_dialog_controls(app)
    except RuntimeError as e:
        log_file.write(str(e) + '\n')
        kill_application(app, log_file)

    # 针对一个随机的控件执行一个针对该控件合法的随机操作
    try:
        execute_a_action(controls, log_file)
    except RuntimeError as e:
        log_file.write(str(e) + '\n')
        kill_application(app, log_file)
    except ValueError as e:
        window = app.top_window()
        children_item = window.children()
        for child in children_item:
            log_file.write(str(child.get_properties()) + '\n')

        log_file.write(str(e) + '\n')
        kill_application(app, log_file)

    # 某些操作可能导致当前测试的应用被关闭
    try :
        if not app.top_window().is_visible():
            kill_application(app, log_file)
    except RuntimeError as e:
        log_file.write(str(e) + '\n')
        kill_application(app, log_file)
    """    
        
def kill_application(app, log_file):
    log_file.close()
    app.kill()
    sys.exit(0)

def screen_capture_and_exit(app, log_file):
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    kill_application(app, log_file)

def change_to_status_2(app, log_file):
    
    window = app.top_window()
    window.wait('ready')
    
    # 当前页面可能会被文件模态弹窗覆盖，导致测试失效，需要首先关闭模态弹窗
    button = window.child_window(title="取消", control_type="Button")
    if button.exists():
        button.click_input(button='left')
        window = app.top_window()
        window.wait('ready')

    # 当前页面可能会被模态弹窗覆盖，导致测试失效，需要首先关闭模态弹窗
    button = window.child_window(title="Cancel", control_type="Button")
    if button.exists():
        button.click_input(button='left')
        window = app.top_window()
        window.wait('ready')

    # 非模态弹窗可能会覆盖其他按键的显示，需要关闭
    item = window.child_window(title="Power-PI", control_type="Window", class_name="CurvePlotting")
    if item.exists():
        button = item.child_window(title="关闭", control_type="Button")
        if button.exists():
            button.click_input(button='left')

    # 切换到文件tab页
    item = window.child_window(title="文件", control_type="TabItem")
    if item.exists():
        item.click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    # 通过导入工程文件按钮导入工程文件
    window = app.top_window()
    window.wait('ready')
    button = window.child_window(title="导入工程", control_type="Button")
    if button.exists():
        button.click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    # 如果之前的测试逻辑没出问题的话，当前的文件对话框的路径应该为当前文件夹
    # 移动到对应的工程文件夹
    window = app.top_window()
    window.wait('ready')
    button = window.child_window(title="上移到“viewer_auto_test”(Alt + 向上键)", control_type="Button")
    if button.exists():
        button.click_input(button='left')
    else:
        print(222)
        screen_capture_and_exit(app, log_file)

    window = app.top_window()
    window.wait('ready')
    item = window.child_window(title="project_demo", control_type="ListItem")
    if item.exists():
        item.double_click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    window = app.top_window()
    window.wait('ready')
    item = window.child_window(title="vessel.ppp", control_type="ListItem")
    if item.exists():
        item.double_click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    # 完整状态切换后休眠一段时间以确保后台线程都完成各自的任务执行
    time.sleep(5)


def change_to_status_3(app, log_file):
    
    window = app.top_window()
    window.wait('ready')

    # 当前页面可能会被文件模态弹窗覆盖，导致测试失效，需要首先关闭模态弹窗
    button = window.child_window(title="取消", control_type="Button")
    if button.exists():
        button.click_input(button='left')
        window = app.top_window()
        window.wait('ready')

    # 当前页面可能会被模态弹窗覆盖，导致测试失效，需要首先关闭模态弹窗
    button = window.child_window(title="Cancel", control_type="Button")
    if button.exists():
        button.click_input(button='left')
        window = app.top_window()
        window.wait('ready')

    # 非模态弹窗可能会覆盖其他按键的显示，需要关闭
    item = window.child_window(title="Power-PI", control_type="Window", class_name="CurvePlotting")
    if item.exists():
        button = item.child_window(title="关闭", control_type="Button")
        if button.exists():
            button.click_input(button='left')

    # 切换到工作tab页
    item = window.child_window(title="工作台", control_type="TabItem")
    if item.exists():
        item.click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    # 导入后处理文件
    window = app.top_window()
    window.wait('ready')
    button = window.child_window(title="单文件导入", control_type="Button")
    if button.exists():
        button.click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    window = app.top_window()
    window.wait('ready')
    button = window.child_window(title="上移到“viewer_auto_test”(Alt + 向上键)", control_type="Button")
    if button.exists():
        button.click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    window = app.top_window()
    window.wait('ready')
    item = window.child_window(title="data", control_type="ListItem")
    if item.exists():
        item.double_click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    window = app.top_window()
    window.wait('ready')
    item = window.child_window(title="vtk", control_type="ListItem")
    if item.exists():
        item.double_click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    window = app.top_window()
    window.wait('ready')
    item = window.child_window(title="test.vts", control_type="ListItem")
    if item.exists():
        item.double_click_input(button='left')
    else:
        screen_capture_and_exit(app, log_file)

    # 完整状态切换后休眠一段时间以确保后台线程都完成各自的任务执行
    time.sleep(5)


def main():
    application_path = str(sys.argv[1])
    total_test_count = int(sys.argv[2])

    app = execute_application(application_path)
    current_test_times = 1

    # 创建日志文件夹
    if not os.path.exists("./ui_monkey_log/"):
        os.makedirs("./ui_monkey_log/")

    # 状态1测试，状态1为初态
    # 打开全局日志文件
    log_file_1 = open("./ui_monkey_log/log_status_1.txt", mode='w')
    while current_test_times <= total_test_count:
        try:
            monkey_test(app, log_file_1)
            current_test_times += 1
        except RuntimeError as e:
            if str(e) == "No windows for that process could be found":
                log_file_1.write(str(e) + '\n')
                kill_application(app, log_file_1)
        except Exception as e:
            log_file_1.write(str(e) + '\n')
            continue
    log_file_1.close()
    print("status 1 test finish")
    
    # 状态2测试，状态2为计算任务发起前的状态，即计算配置完成，网格导入后的状态
    current_test_times = 1
    log_file_2 = open("./ui_monkey_log/log_status_2.txt", mode='w')
    change_to_status_2(app, log_file_2)

    while current_test_times <= total_test_count:
        try:
            monkey_test(app, log_file_2)
            current_test_times += 1
        except RuntimeError as e:
            if str(e) == "No windows for that process could be found":
                log_file_2.write(str(e) + '\n')
                kill_application(app, log_file_2)
        except Exception as e:
            log_file_2.write(str(e) + '\n')
            continue
    log_file_2.close()
    print("status 2 test finish")
    
    # 状态3测试，状态3为计算任务发起后的状态，即计算配置完成，网格导入，后处理结果导入后的状态
    current_test_times = 1
    log_file_3 = open("./ui_monkey_log/log_status_3.txt", mode='w')
    change_to_status_3(app, log_file_3)

    while current_test_times <= total_test_count:
        try:
            monkey_test(app, log_file_3)
            current_test_times += 1
        except RuntimeError as e:
            if str(e) == "No windows for that process could be found":
                log_file_3.write(str(e) + '\n')
                kill_application(app, log_file_3)
        except Exception as e:
            log_file_3.write(str(e) + '\n')
            continue
    log_file_3.close()
    print("status 3 test finish")

    app.kill()


# 调用主函数
if __name__ == "__main__":
    main()
