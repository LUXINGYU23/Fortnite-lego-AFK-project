from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController, GlobalHotKeys
import random
import time
import threading
import win32gui
import win32con
from pynput import keyboard
import win32api
import win32con

# 打印版权信息
print("作者 / Author: 北海无河")
print("日期 / Date: 2024.12.8")
print("描述 / Description: 这是一个用于控制Fortnite游戏乐高模式的挂机脚本，实现了鼠标和键盘的自动控制。同时允许用户通过快捷键开启和关闭挂机功能，同时不影响用户自身鼠标键盘输入使用。")
print("This is an AFK script for Fortnite LEGO mode, implementing automatic mouse and keyboard control. Users can toggle the AFK function with hotkeys while retaining normal mouse and keyboard usage.")
print("版本 / Version: 1.0, 仅供学习交流使用 / For learning and communication purposes only")
print("免责声明 / Disclaimer: 本程序仅供学习交流使用，作者不对使用本程序导致的任何后果负责。")
print("This program is for learning purposes only. The author is not responsible for any consequences of using this program.")
print("版权 / Copyright: 本程序版权归作者所有，未经作者许可，不得用于任何商业用途，否则后果自负！")
print("All rights reserved. Commercial use without author's permission is prohibited!")
print("CopyRight © 2024 北海无河. All Rights Reserved.")
print("--------------------------------------------------")
# 使用说明
print("使用说明 / Instructions:")
print("1. 请确保Fortnite窗口已经打开 / Make sure Fortnite window is open")
print("2. 按下 <ctrl>+<f9> 开启挂机功能 / Press <ctrl>+<f9> to start AFK mode")
print("3. 按下 <ctrl>+<f10> 关闭挂机功能 / Press <ctrl>+<f10> to stop AFK mode")
print("4. 按下 <ctrl>+<c> 退出程序 / Press <ctrl>+<c> to exit program")
print("5. 进入乐高模式后再开启挂机功能，然后按住WIN键切换到其他窗口使用键鼠，挂机功能会自动运行")
print("   Enter LEGO mode before starting AFK mode, then hold WIN key to switch to other windows. The AFK function will run automatically")

# 全局变量
running = False
fortnite_window = None  # 改名
mouse = MouseController()
keyboard = KeyboardController()
movement_thread = None  # 添加这一行

# 添加新的全局变量
MOVEMENT_PATTERNS = [
    ['w'], ['w', 'space'], ['w', 'a'], ['w', 'd'],
    ['a'], ['d'], ['s'], ['w', 'shift']
]
ACTION_COOLDOWNS = {
    'jump': 3,
    'build': 5,
    'attack': 2,
    'interact': 4
}
last_actions = {key: 0 for key in ACTION_COOLDOWNS}


def find_fortnite_window():
    global fortnite_window
    # 通过UnrealWindow类名查找Fortnite窗口
    fortnite_window = win32gui.FindWindow("UnrealWindow", None)
    if fortnite_window and win32gui.IsWindowVisible(fortnite_window):
        print(f"找到Fortnite窗口! 窗口句柄: {fortnite_window}")
        return True
    return False

def move_mouse_randomly():
    global running
    while running:
        if fortnite_window:  # 改名
            rect = win32gui.GetWindowRect(fortnite_window)
            x1, y1, x2, y2 = rect
            
            center_x = (x2 + x1) // 2
            center_y = (y2 + y1) // 2
            
            delta_x = random.randint(-200, 200)
            delta_y = random.randint(-100, 100)
            
            target_x = center_x + delta_x
            target_y = center_y + delta_y
            lParam = win32api.MAKELONG(target_x, target_y)
            win32api.PostMessage(fortnite_window, win32con.WM_MOUSEMOVE, 0, lParam)
            print(f"Moved mouse to ({target_x}, {target_y})")
        time.sleep(random.uniform(0.3, 1.0))

def press_keys_randomly():
    global running
    movement_keys = {'w': 0x57, 'a': 0x41, 's': 0x53, 'd': 0x44}
    action_keys = {Key.space: win32con.VK_SPACE, Key.shift: win32con.VK_SHIFT, 'e': 0x45, 'r': 0x52, 'f': 0x46}
    
    while running:
        if fortnite_window:  # 改名
            if random.random() < 0.8:
                key = random.choice(list(movement_keys.keys()))
                vk = movement_keys[key]
                win32api.PostMessage(fortnite_window, win32con.WM_KEYDOWN, vk, 0)
                print(f"Key down: {key}")
                time.sleep(random.uniform(0.5, 2))
                win32api.PostMessage(fortnite_window, win32con.WM_KEYUP, vk, 0)
                print(f"Key up: {key}")
            
            if random.random() < 0.4:
                key = random.choice(list(action_keys.keys()))
                vk = action_keys[key]
                win32api.PostMessage(fortnite_window, win32con.WM_KEYDOWN, vk, 0)
                win32api.PostMessage(fortnite_window, win32con.WM_KEYUP, vk, 0)
                print(f"Pressed key: {key}")
            
            if random.random() < 0.3:
                win32api.PostMessage(fortnite_window, win32con.WM_LBUTTONDOWN, win32con.VK_LBUTTON, 0)
                print("Mouse down")
                time.sleep(random.uniform(0.1, 0.5))
                win32api.PostMessage(fortnite_window, win32con.WM_LBUTTONUP, win32con.VK_LBUTTON, 0)
                print("Mouse up")
        
        time.sleep(random.uniform(0.2, 0.8))

def simulate_natural_movement():
    global running
    while running:
        if fortnite_window:  # 改名
            # 选择一个随机的移动模式
            pattern = random.choice(MOVEMENT_PATTERNS)
            duration = random.uniform(0.5, 2.0)
            
            # 按下所有键
            for key in pattern:
                if len(key) == 1:
                    vk = ord(key.upper())
                else:
                    vk = getattr(win32con, f'VK_{key.upper()}')
                win32api.PostMessage(fortnite_window, win32con.WM_KEYDOWN, vk, 0)
                time.sleep(random.uniform(0.05, 0.2))  # 添加随机时延
            
            # 模拟视角随机移动
            start_time = time.time()
            while time.time() - start_time < duration and running:
                delta_x = random.randint(-50, 50)
                delta_y = random.randint(-20, 20)
                simulate_mouse_movement(delta_x, delta_y)
                time.sleep(0.05)
            
            # 释放所有键
            for key in pattern:
                if len(key) == 1:
                    vk = ord(key.upper())
                else:
                    vk = getattr(win32con, f'VK_{key.upper()}')
                win32api.PostMessage(fortnite_window, win32con.WM_KEYUP, vk, 0)
                time.sleep(random.uniform(0.05, 0.2))  # 添加随机时延
            
            # 随机执行动作
            perform_random_action()
        
        time.sleep(random.uniform(0.1, 0.3))

def simulate_mouse_movement(dx, dy):
    if fortnite_window:  # 改名
        rect = win32gui.GetWindowRect(fortnite_window)
        x1, y1, x2, y2 = rect
        center_x = (x2 + x1) // 2
        center_y = (y2 + y1) // 2
        
        # 使用平滑的鼠标移动
        steps = 5
        for i in range(steps):
            current_x = center_x + (dx * (i + 1) // steps)
            current_y = center_y + (dy * (i + 1) // steps)
            lParam = win32api.MAKELONG(current_x, current_y)
            win32api.PostMessage(fortnite_window, win32con.WM_MOUSEMOVE, 0, lParam)
            time.sleep(0.01)

def perform_random_action():
    current_time = time.time()
    
    # 随机跳跃
    if current_time - last_actions['jump'] > ACTION_COOLDOWNS['jump'] and random.random() < 0.3:
        win32api.PostMessage(fortnite_window, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
        time.sleep(0.1)
        win32api.PostMessage(fortnite_window, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
        last_actions['jump'] = current_time
    
    # 随机攻击
    if current_time - last_actions['attack'] > ACTION_COOLDOWNS['attack'] and random.random() < 0.4:
        win32api.PostMessage(fortnite_window, win32con.WM_LBUTTONDOWN, win32con.VK_LBUTTON, 0)
        time.sleep(random.uniform(0.1, 0.3))
        win32api.PostMessage(fortnite_window, win32con.WM_LBUTTONUP, win32con.VK_LBUTTON, 0)
        last_actions['attack'] = current_time

def on_activate_start():
    global running, movement_thread
    if not running:
        running = True
        print("挂机功能已开启")
        movement_thread = threading.Thread(target=simulate_natural_movement)
        movement_thread.start()

def on_activate_stop():
    global running, movement_thread
    if running:
        running = False
        print("挂机功能已关闭")
        if movement_thread and movement_thread.is_alive():
            movement_thread.join()
            movement_thread = None

hotkeys = GlobalHotKeys({
    '<ctrl>+<f9>': on_activate_start,
    '<ctrl>+<f10>': on_activate_stop
})

hotkeys.start()

if __name__ == "__main__":
    try:
        print("\n正在等待Fortnite窗口打开... / Waiting for Fortnite window to open...")
        print("提示: 请先启动Fortnite游戏，进入大厅后再运行此脚本")
        print("Tip: Please launch Fortnite and enter the lobby before running this script\n")
        
        while True:
            if find_fortnite_window():
                print("成功检测到Fortnite窗口! / Successfully detected Fortnite window!")
                print("你现在可以: / You can now:")
                print("1. 进入乐高模式 / Enter LEGO mode")
                print("2. 按下 <ctrl>+<f9> 开启挂机 / Press <ctrl>+<f9> to start AFK")
                print("3. 按下 <ctrl>+<f10> 关闭挂机 / Press <ctrl>+<f10> to stop AFK")
                break
            else:
                print("未检测到Fortnite窗口，3秒后重试... / Fortnite window not detected, retrying in 3 seconds...")
                time.sleep(3)
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
        if movement_thread and movement_thread.is_alive():
            movement_thread.join()
        hotkeys.stop()
        print("\n程序已退出！/ Program exited!")