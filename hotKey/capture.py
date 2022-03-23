from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import cv2
import win32gui
import time
from window import move_window,resize_window,resize_client
from mouse import leftClick
import threading
import os

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
        for i in filenames :
            if i.endswith('.png'):
                picPath = os.path.join(dirpath,i)
                picPath_list.append(picPath)
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
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # 读取图片，并保留Alpha通道
    template = cv2.imread('bar8.png', cv2.IMREAD_UNCHANGED)
    # 取出Alpha通道
    alpha = template[:, :, 3]
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
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
    point = getPoint(handle,path)
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
            x = i * 960
            y = 0
        x = round(x)
        y = round(y)
        handle = handles[i]
        resize_window(handle, 960, 540)
        # resize_client(handle, 900, 500)
        move_window(handle,x,y)
def play(handle):
    while True:
        pic_list = get_picPath()
        for pic in pic_list:
            searchAndClick(handle,pic)
            time.sleep(1/len(pic_list))


if __name__ == "__main__":
    handles = []
    handles += get_handles_id("MG Asia - Google Chrome")
    handles += get_handles_id("Egret - Google Chrome")
    handles += get_handles_id("Bobao Gaming - Google Chrome")
    handles += get_handles_id("MG Asia - Google Chrome")
    init_windows(handles)
    lock = threading.Lock()
    for handle in handles:
        print(handle)
        cutPic(handle,677,489,724,510)
    #     t = threading.Thread(target=play,args=(handle,))
    #     t.start()
    #     time.sleep(3)
    # resize_window(handle,960,540)
    # # move_window(handle,0,0)
    # # point = getPoint(handle,path = 'test5.png')
    # # print(point)