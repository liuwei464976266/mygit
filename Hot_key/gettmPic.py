import cv2

# 修改透明背景为白色
def transparence2white(img1,img2):
    sp1=img1.shape  # 获取图片维度
    width1=sp1[0]  # 宽度
    height1=sp1[1]  # 高度
    for yh1 in range(height1):
        for xw1 in range(width1):
            color_d1=img1[xw1,yh1] # 遍历图像每一个点，获取到每个点4通道的颜色数据

            color_d2 = img2[xw1, yh1]
            if color_d1[0] != color_d2[0] or color_d1[1] != color_d2[1] or color_d1[2] != color_d2[2]:
                print('yichang')
                img1[xw1, yh1] = [color_d1[0], color_d1[1], color_d1[2], 0]  # 则将当前点的颜色设置为白色，且图像设置为不透明
                    # if(color_d[3]==0):  # 最后一个通道为透明度，如果其值为0，即图像是透明
                    #     img[xw,yh]=[255,255,255,255]  # 则将当前点的颜色设置为白色，且图像设置为不透明
    return img1

img1=cv2.imread('test2.png',cv2.IMREAD_UNCHANGED)  # 读取图片。-1将图片透明度传入，数据由RGB的3通道变成4通道
img2 = cv2.imread('t4.png',cv2.IMREAD_UNCHANGED)
img=transparence2white(img1,img2)  # 将图片传入，改变背景色后，返回
cv2.imwrite('test3.png',img)  # 保存图片，文件名自定义，也可以覆盖原文件