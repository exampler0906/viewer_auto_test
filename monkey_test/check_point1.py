from pywinauto.application import Application
from pywinauto import Desktop

# Power-Pi路径 请修改为自己的路径
powerpiPath = 'C:\\Users\\karl\\Downloads\\#199-Release\\Release\\Power-PI.exe'

# 网格文件路径 请修改为自己的路径
gridFilePath = 'C:\\Users\\karl\\Downloads\\#199-Release\\Release\\project_demo\\manifold_2Mpa\\manifold_2Mpa.ppu'

apps = Application(backend='uia')
windows = Desktop(backend='uia')

# 判断Power-PI是否已经运行
is_running = False
for window in windows.windows():
    if 'Power-PI' in window.window_text():
        is_running = True

# 如果Power-PI已经运行，则连接Power-PI
# 如果Power-PI未运行，则启动Power-PI
if is_running:
    apps.connect(path=powerpiPath)
else:
    apps.start(powerpiPath)

# 获得Power-PI主窗口
dlg = apps['powerpi']

# Check point1-1：导入网格
# 如果Power-PI未运行，则自动导入网格文件
if not is_running:
    dlg['文件'].click_input(button='left')
    dlg['导入网格'].click_input(button='left')
    dlg['文件名(N):Edit'].type_keys(gridFilePath)
    dlg['打开(O)Button'].click_input(button='left')
else:
    pass

# TODO Check point1-2：网格显示隐藏
# Check point1-2：网格显示隐藏
# 暂未实现，无法找到隐藏按钮
dlg['模拟TreeView'].manifold_2Mpa.print_control_identifiers()

# Check point1-3：网格属性变更
dlg['模拟TreeView'].manifold_2Mpa.click_input(button='left')
dlg['opacityEdit'].type_keys('{BACKSPACE}')
dlg['opacityEdit'].type_keys('0')
dlg['opacity'].click_input(button='left')
# 还原Check point1-3中变更的属性
dlg['opacityEdit'].type_keys('{BACKSPACE}')
dlg['opacityEdit'].type_keys('1')
dlg['opacity'].click_input(button='left')

# Check point1-4：网格渲染模式及方向变更
dlg['工作台'].click_input(button='left')
dlg['正x方向'].click_input(button='left')

# Check point1-5：网格重命名
"""
两次执行dlg['工作台'].click_input(button='left')时
第一次会点击到“几何”tab上
第二次则会点击搭到“工作台”tab上
"""
dlg['模拟TreeView'].manifold_2Mpa.double_click_input(button='left')
dlg['模拟TreeView'].manifold_2Mpa.type_keys('{BACKSPACE}')
dlg['模拟TreeView'].manifold_2Mpa.type_keys('manifold_2Mpa111')
dlg['工作台'].click_input(button='left')
# 还原Check point1-5中变更的属性
dlg['模拟TreeView'].manifold_2Mpa.double_click_input(button='left')
dlg['模拟TreeView'].manifold_2Mpa.type_keys('{BACKSPACE}')
dlg['模拟TreeView'].manifold_2Mpa.type_keys('manifold_2Mpa')
dlg['工作台'].click_input(button='left')

# Check point1-6：网格删除
dlg['模拟TreeView'].manifold_2Mpa.click_input(button='right')
dlg['删除MenuItem'].click_input(button='left')
