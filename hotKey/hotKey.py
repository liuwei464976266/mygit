#!/usr/bin/env python3
import sys
sys.path.append(r'D:\pytest\key')
import win32con
import ctypes
import ctypes.wintypes
from threading import Thread, activeCount, enumerate
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import cv2,os
import win32gui
import time
import logAnalysisUtil
from window import move_window,resize_window, resize_client
from mouse import leftClick
import threading, os, addGold
GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC

# 防止UI放大导致截图不完整
windll.user32.SetProcessDPIAware()
def get_picPath(path = "."):
    picPath_list = []
    for dirpath,dirnames,filenames in os.walk(path):
        for i in filenames:
            if i.endswith('.png'):
                pic_path = os.path.join(path,i)
                picPath_list.append(pic_path)
        break
    return picPath_list
def capture(handle: HWND):
    """窗口客户区截图

    Args:
        handle (HWND): 要截图的窗口句柄

    Returns:
        numpy.ndarray: 截图数据
    """
    # 获取窗口客户区的大小
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    # 开始截图
    dc = GetDC(handle)
    cdc = CreateCompatibleDC(dc)
    bitmap = CreateCompatibleBitmap(dc, width, height)
    SelectObject(cdc, bitmap)
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    # 截图是BGRA排列，因此总元素个数需要乘以4
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    # 返回截图数据为numpy.ndarray
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
def cutPic(handle,x1,y1,x2,y2):
    """
        目标区域截图
    """
    img = capture(handle)
    im = img[y1:y2, x1:x2]
    timeStamp = time.time()
    save_path = str(timeStamp) + '.png'
    cv2.imwrite(save_path, im)
def getPoint(handle,path):#获取图片坐标
    image = capture(handle)
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # 读取图片，并保留Alpha通道
    template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    # 取出Alpha通道
    # try:
    #     alpha = template[:, :, 3]
    #     result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
    # except:
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED)
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配

    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if 0.99 <= max_val <= 1:
        top_left = max_loc
        print(threading.current_thread(),handle,'->',path,top_left)
        return top_left
    else:
        return (-1,-1)
# def getPoint(handle,path):
#     image = capture(handle)
#     # 转为灰度图
#     gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
#     # 读取图片，并保留Alpha通道
#     template = cv2.imread(path, 0)
#     # 取出Alpha通道
#     # alpha = template[:, :, 3]
#     template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
#     # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
#     result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
#     # 获取结果中最大值和最小值以及他们的坐标
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     print(min_val, max_val, min_loc, max_loc)
#     if 1 <= max_val <= 2:
#         top_left = max_loc
#         return top_left
#     else:
#         return (-1,-1)
def searchAndClick(handle,path):
    lock.acquire()
    point = getPoint(handle, path)
    if point != (-1,-1):
        x = point[0]
        y = point[1]
        leftClick(handle,x,y)
    lock.release()
def get_handles_id(title):
    '''
    根据标题找句柄
    :param title: 标题
    :return:返回句柄所对应的ID
    '''
    jh = []
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t != "":
            if title in t:
                jh.append(h)
    if len(jh) == 0:
        return []
    else:
        return jh
def init_windows(handles):
    handlesLength = len(handles)
    for i in range(handlesLength):
        if handlesLength > 2:
            if i < handlesLength / 2:
                lens = handlesLength
                halflen = lens / 2 + 0.1
                qzhalflen = round(halflen)
                x = (960 / (qzhalflen - 1)) * i
                y = 0
            else:
                lens = handlesLength
                halflen = lens / 2 + 0.1
                qzhalflen = round(halflen)
                chi = i - qzhalflen
                fg = 960 / (qzhalflen - 1)
                x = chi * fg
                y = 540
        else:
            x = 0
            y = i * 540
        x = round(x)
        y = round(y)
        handle = handles[i]
        resize_window(handle, 960, 540)
        move_window(handle,x,y)
class Hotkey(Thread):
    user32 = ctypes.windll.user32
    hkey_list = {}
    hkey_flags = {}  # 按下
    hkey_running = {}  # 启停
    _reg_list = {}  # 待注册热键信息

    def regiskey(self, hwnd=None, flagid=0, fnkey=win32con.MOD_ALT, vkey=win32con.VK_F9):  # 注册热键，默认一个alt+F9
        return self.user32.RegisterHotKey(hwnd, flagid, fnkey, vkey)

    def get_reginfo(self):
        return self._reg_list

    def get_id(self, func):
        self_id = None
        for id in self.get_reginfo():
            if self.get_reginfo()[id]["func"] == func:
                self_id = id
                break
        if self_id:
            self.hkey_running[self_id] = True
        return self_id

    def get_running_state(self, self_id):
        if self.hkey_running.get(self_id):
            return self.hkey_running[self_id]
        else:
            return False

    def reg(self, key, func, args=None):
        id = int(str(round(time.time() * 10))[-6:])
        fnkey = key[0]
        vkey = key[1]
        info = {
            "fnkey": fnkey,
            "vkey": vkey,
            "func": func,
            "args": args
        }
        self._reg_list[id] = info
        # print(info) #这里待注册的信息
        time.sleep(0.1)
        return id

    def fast_reg(self, id, key=(0, win32con.VK_HOME), func=lambda: print('热键注册开始')):
        if not self.regiskey(None, id, key[0], key[1]):
            print("热键注册失败")
            return None
        self.hkey_list[id] = func
        self.hkey_flags[id] = False
        return id

    def callback(self):
        def inner(self=self):
            for flag in self.hkey_flags:
                self.hkey_flags[flag] = False

            while True:
                for id, func in self.hkey_list.items():
                    if self.hkey_flags[id]:
                        args = self._reg_list[id]["args"]
                        if args:
                            # print(args)  #这里打印传入给注册函数的参数
                            thread_it(func, *args)
                        else:
                            thread_it(func)
                        self.hkey_flags[id] = False

        return inner

    def run(self):
        for id in self._reg_list:
            reg_info = self._reg_list[id]
            fnkey = reg_info["fnkey"]
            vkey = reg_info["vkey"]
            func = reg_info["func"]
            self.fast_reg(id, (fnkey, vkey), func)

        fn = self.callback()
        thread_it(fn)  # 启动监听热键按下线程

        try:
            msg = ctypes.wintypes.MSG()
            while True:
                if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam in self.hkey_list:
                            self.hkey_flags[msg.wParam] = True
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            for id in self.hkey_list:
                self.user32.UnregisterHotKey(None, id)

def thread_it(func, *args):
    t = Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

def play(handle):
    global runningEnble
    userName_handle = {1377700: '241_s12349', 1376940: '241_s12350', 1902536: '241_s12351', 2818724: '241_s12352'}
    while runningEnble:
        pic_list = get_picPath(r'D:\pytest\pic')
        for pic in pic_list:
            print(pic)
            searchAndClick(handle, pic)
            time.sleep(1 / len(pic_list))
        # special_pic_list = get_picPath(r"D:\pytest\pic")
        # for pic in special_pic_list:
        #     point = getPoint(handle, pic)
        #     if point != (-1, -1):
        #         x = point[0]
        #         y = point[1]
        #         userName = userName_handle.get(handle)
        #         addGold.userGoldControl(target_gold = 16,userName=userName)
        #         time.sleep(2)
        #         leftClick(handle, x, y)
        #         break
    print(f'{threading.current_thread()} 线程结束')
def jump(func, hotkey):
    global runningEnble,lock
    self_id = hotkey.get_id(func)
    handles = []
    handles += get_handles_id("MG Asia - Google Chrome")
    handles += get_handles_id("Egret - Google Chrome")
    handles += get_handles_id("Bobao Gaming - Google Chrome")
    handles += get_handles_id("MG Asia - Google Chrome")
    init_windows(handles)
    lock = threading.Lock()
    runningEnble = True
    for handle in handles:
        t = threading.Thread(target=play,args=(handle,))
        time.sleep(3)
        t.start()
    while hotkey.get_running_state(self_id):
        time.sleep(1)
    runningEnble = False

def stop_jump(start_id, hotkey):
    hotkey.hkey_running[start_id] = False
    print(f"{start_id} 即将停止")
    time.sleep(10)
    print(f'当前线程列表:{activeCount()}', enumerate())
    exit(-2)


def main():
    hotkey = Hotkey()
    start_id = hotkey.reg(key=(win32con.MOD_ALT, win32con.VK_HOME), func=jump, args=(jump, hotkey))  # alt home键 开始
    hotkey.reg(key=(0, win32con.VK_END), func=stop_jump, args=(start_id, hotkey))  # alt end键 结束
    hotkey.start()  # 启动热键主线程

    print(f"当前总线程数量:{activeCount()}")
    print('当前线程列表:', enumerate())
    print('热键注册初始化完毕，尝试按组合键alt+Home 或者单键END看效果')


if __name__ == '__main__':
    main()