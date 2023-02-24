import cv2
import numpy as np

# 加载图像
image = cv2.imread("./imgs/wexin_test1.jpg")

# 灰度化处理
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二值化处理
ret, img_obj= cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 腐蚀操作
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
eroded = cv2.erode(thresh, kernel)

# 寻找轮廓
contours, hierarchy = cv2.findContours(
    eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 遍历所有轮廓
for idx, contour in enumerate(contours):
    # 计算轮廓面积
    area = cv2.contourArea(contour)

    # 忽略太小的轮廓
    if area < 100:
        continue

    # 计算轮廓的外接矩形
    rect = cv2.minAreaRect(contour)

    # 将矩形转换为box
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # 计算box的宽和高
    width = np.linalg.norm(box[0] - box[1])
    height = np.linalg.norm(box[1] - box[2])

    # 忽略不是题目的矩形
    # if width < 100 or height < 100 or width > 1000 or height > 1000:
    #     continue

    # 对题目区域进行透视变换
    src_pts = box.astype("float32")
    dst_pts = np.array([[0, 0], [0, height], [width, height], [
                       width, 0]], dtype="float32")
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(gray, M, (int(width), int(height)))

    # 显示切割出来的题目
    cv2.imwrite("./result/output_" + str(idx) + ".png", warped)
