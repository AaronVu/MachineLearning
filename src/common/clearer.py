# -*- coding:utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt


def convolution(img_path):
    '''
    图解卷积:
    1将两个函数都用x表示
    2对其中一个函数做水平翻转:g(x)->g(-x)
    3加上一个事件偏移量，让g(t-x)随着x轴移动
    4让t从负无穷滑动到正无穷，两个函数交会时
    下面使用平均滤波器，5*5
            1   1   1   1   1
            1   1   1   1   1
    K=1/25  1   1   1   1   1
            1   1   1   1   1
    将核放在图像的像素A上，求与核对应的图像上25(5*5)个像素的和，再取平均数
    用平均数代替像素A的值，重复以上操作直到将图像的每一个像素值都更新一遍
    '''
    img = cv2.imread(img_path)
    '''
    numpy.ones(shape,dtype=None):
    shape是(行数，列数)，即(高度，宽度)
    dtype:数据类型，例如 np.float32
    '''
    kernel = np.ones((5,5) , np.float32) / 25
    '''
    cv2.filter2D(src,ddepth , kernel)
    ddepth:要求的目标图像的深度，如果为-1，表示与原图像深度相同
    kernel:卷积核,实质是一个矩阵。卷积时使用到的权用一个矩阵表示，该矩阵与使用的图像区域大小相同，行列都是奇数，是一个矩阵
    '''
    dst = cv2.filter2D(img , -1 , kernel)
    plt.subplot(121),plt.imshow(img),plt.title("Original Image")
    plt.xticks([]),plt.yticks([])
    plt.subplot(122),plt.imshow(dst),plt.title("Average Convolution")
    plt.xticks([]),plt.yticks([])
    plt.show()


def averageConvolution(img_path):
    '''
    图像模糊（图像平滑）
    低通滤波器可以模糊图像，去除噪音（高频成分，边界会被模糊）
    平均：归一化卷积框完成。用卷积框覆盖区域所有像素的平均值来代替中心元素，使用函数cv2.blur()
         cv2.boxFilter()，需要设定卷积框的宽和高
    下面是3*3的归一化卷积框
            1   1   1
    K=1/9   1   1   1
            1   1   1
    如果不想使用归一化卷积框，应该使用cv2.boxFilter(),传入参数normalize=False
    '''
    img = cv2.imread(img_path)
    '''
    cv2.blur(src,ksize[,dst[,anchor[,borderTyppe]]])->dst
    作用：使用核来平滑（模糊）图像
    ksize:是包含宽度和高度的二元组。例如(3,3)
    anchor:锚点，中心点，默认为(-1,-1)则会选取核的中心点
    borderType:边界模式用于推断图像外的像素
    K=/(ksize.width * ksize.height)[1 1 ...1]
                                    [1 1 ...1]
                                    [1 1 ...1]
    '''
    blur = cv2.blur(img , (5,5))
    plt.subplot(121),plt.imshow(img),plt.title("Original Image")
    plt.xticks([]),plt.yticks([])
    plt.subplot(122),plt.imshow(blur),plt.title("Blured Image")
    plt.xticks([]),plt.yticks([])
    plt.show()


def GaussianBlur_test(img_path):
    '''
    高斯模糊
    把卷积和换成高斯核（自我认为是高斯核一个加权矩阵，主要用于乘以原来图像中的像素的值然后求和）
    实现的函数是cv2.GaussianBlur()，需要指定高斯核的宽和高，都是奇数，
    以及高斯函数沿着x轴和y轴的标准差，也可以使用cv2.getGaussianKernel()自己构建一个高斯核
    '''
    img = cv2.imread(img_path)
    #img = cv2.imread("bilateralFilter.jpg")
    '''
    cv2.GaussianBlur(src,ksize,sigmaX)
    kSize:核大小,sigmaX:高斯核在x轴的标准差,如果为0会根据核的宽和高重新计算
    '''
    blur = cv2.GaussianBlur(img , (5,5) , 0)
    plt.subplot(121),plt.imshow(img),plt.title("Original Image")
    plt.xticks([]),plt.yticks([])
    plt.subplot(122),plt.imshow(blur),plt.title("GaussianBlured Image")
    plt.xticks([]),plt.yticks([])
    plt.show()


def BilateralFilter_test(img_path):
    '''
    双边滤波:
    能保持边界清晰的情况下有效去除噪音，比其他滤波器慢
    双边滤波同时使用空间高斯权重和灰度值相似性高斯权重。
    空间高斯函数确保只有邻近区域的像素对中心点有影响，灰度值相似性高斯
    函数确保只有与中心像素灰度值相近的才会被用来做模糊运算。
    cv2.bilateralFilter()
    '''
    img = cv2.imread(img_path)
    '''
    cv2.bilateralFilter(src,d,sigmaColor,sigmaSpace)
    d:过滤中使用的每个像素邻域的直径
    sigmaColor:用于颜色过滤，sigmaSpace:用于空间过滤
    '''
    #9是邻域直径，两个75分别是空间高斯函数标准差，灰度值相似标准差
    blur = cv2.bilateralFilter(img , 9 , 75 ,75)
    plt.subplot(121),plt.imshow(img),plt.title("Original Image")
    plt.xticks([]),plt.yticks([])
    plt.subplot(122),plt.imshow(blur),plt.title("BilateralFilter Image")
    plt.xticks([]),plt.yticks([])
    plt.show()


def MedianBlur_test(img_path):
    '''
    中值模糊：用卷积框对应像素的中值代替中心像素的值，用于去除椒盐噪声(黑白相间的亮暗点噪声)
    '''
    img = cv2.imread(img_path)
    '''
    cv2.GaussianBlur(src,ksize)
    kSize:核大小,是一个大于1的奇数
    '''
    median = cv2.medianBlur(img , 5)

    plt.subplot(121),plt.imshow(img),plt.title("Original Image")
    plt.xticks([]),plt.yticks([])
    plt.subplot(122),plt.imshow(median),plt.title("MedianBlured Image")
    plt.xticks([]),plt.yticks([])
    plt.show()


from PIL import Image, ImageFilter

if __name__ == "__main__":
    # convolution('timg.jpg')
    # averageConvolution('timg.jpg')
    # GaussianBlur_test('timg.jpg')
    # MedianBlur_test('timg.jpg')
    # BilateralFilter_test('timg.jpg')
    img = Image.open('timg.jpg')
    img.filter(ImageFilter.DETAIL)
    img.show()

