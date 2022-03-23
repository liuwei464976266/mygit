from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import time
import pytesseract
# 窗口操作请看https://zhuanlan.zhihu.com/p/363599118
from window import move_window,resize_window,resize_client
# 截图操作请看https://zhuanlan.zhihu.com/p/361569101
from capture import capture
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
if __name__ == "__main__":
    import cv2
    handle = windll.user32.FindWindowW(None, "MG Asia - Google Chrome")
    init_windows((handle,))
    # 加载数字模板
    temps = []
    for i in range(1,10):
        temps.append(cv2.imread(f'nums{i}.png', cv2.IMREAD_GRAYSCALE))

    # 按下任意键退出识别
    while cv2.waitKey(delay=100) == -1:
        im = capture(handle)
        im = im[410:426, 332:376]
        # 提取指定画面中的数字轮廓
        height, width, deep = im.shape
        gray = cv2.cvtColor(im, cv2.COLOR_BGRA2GRAY)
        dst = np.zeros((height, width, 1), np.uint8)
        for i in range(0, height):
            for j in range(0, width):
                grayPixel = gray[i, j]
                dst[i, j] = 255 - grayPixel
        ret, binary = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        string = pytesseract.image_to_string(binary, lang='eng', config='--psm 6 --oem 3 -c '
                                                                        'tessedit_char_whitelist'
                                                         '=0123456789')
        print(string)
        # contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        # result = []
        # for cnt in contours:
        #     [x,y,w,h] = cv2.boundingRect(cnt)
        #     # 按照高度筛选
        #     if 12 > h > 5:
        #         result.append([x,y,w,h])
        #
        # result.sort(key=lambda x:x[0])
        #
        # for x, y, w, h in result:
        #     # 在画面中标记识别的结果
        #     cv2.rectangle(im, (x,y),(x+w,y+h),(0,0,255),1)
        #     digit = cv2.resize(thresh[y:y+h, x:x+w], (14, 20))
        #     res = []
        #     for i, t in enumerate(temps):
        #         score = cv2.matchTemcdplate(digit, t, cv2.TM_CCORR_NORMED)
        #         res.append((i, score[0]))
        #         print((i, score[0]))
        #     res.sort(key=lambda x:x[1])
        #     print(res[-1][0])
        #     cv2.putText(im, str(f"{res[-1][0]}"), (x, y+35), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.putText(dst, string, (0, 0), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.imshow('Digits OCR Test', dst)
