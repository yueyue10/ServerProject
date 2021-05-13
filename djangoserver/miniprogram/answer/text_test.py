# -*- coding: utf-8 -*-
import base64
import json
import os

import cv2
import numpy as np
from imutils.perspective import four_point_transform
from pytesseract import pytesseract
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

hor_space = 20  # 横向间距15
hor_que_space = 15  # 答案单个横向间距
ver_space = 20  # 纵向间距15
ver_que_space = 45  # 答案块纵向间距


class AnswerTest(object):
    def __init__(self, path):
        print("cv2-version========", cv2.__version__)
        self.path = path
        self.file_name = os.path.basename(path)
        # print("file_name", file_name)
        points_file = self.file_name.split(".")[0] + "_points"
        points_file_name = points_file + "." + self.file_name.split(".")[1]
        self.points_file_name = points_file_name  # 选择的答案图片的名称
        self.points_path = os.path.join(os.path.dirname(path), points_file_name)  # 选择的答案的图片路径
        print("path================", self.path)
        print("points_path================", self.points_path)

    def start(self):
        gray_trans, img_trans = self.read_img()
        input_img = self.transform_again(gray_trans, img_trans)
        # 图像清晰度越高结果越精确，时间更长
        # text = pytesseract.image_to_string(input_img, lang="chi_sim")
        # print("pytesseract-text2==", text)
        base_img = self.image_to_base64(input_img)
        text_list = read_text(base_img)
        print("text_list", text_list)
        texts = []
        for text in text_list:
            texts.append(text.DetectedText)
        print("texts=======", texts)

    def read_img(self):
        # 载入并显示图片
        print("self.path==============", self.path)
        img = cv2.imread(self.path)
        wid, hei, _ = img.shape
        img = cv2.resize(img, (int(hei / 2), int(wid / 2)), 0, 0)
        # img = cv2.resize(img, (500, 700), 0, 0)
        self.show_img("img", img)
        # 1.降噪（模糊处理用来减少瑕疵点）
        result = cv2.blur(img.copy(), (5, 5))
        # 2.灰度化,就是去色（类似老式照片）
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # 3.霍夫变换圆检测-定位答题卡圆圈位置
        circles = cv2.HoughCircles(gray.copy(), cv2.HOUGH_GRADIENT, 1, 300, param1=250, param2=15, minRadius=5,
                                   maxRadius=20)
        circles = np.round(circles[0, :]).astype('int')
        circles = sorted(circles, key=lambda x: x[1])  # 对y轴排序
        top_circles = sorted(circles[0: 2], key=lambda x: x[0])  # 对x轴排序
        bottom_circles = sorted(circles[2: 4], key=lambda x: x[0])  # 对x轴排序
        loc_circles = np.vstack((top_circles, bottom_circles))  # 重新组装的定位圆
        # 遍历4个定位圆，取出其有用的坐标
        four_points = []
        for idx, (x, y, r) in enumerate(loc_circles):
            # 绘制圆和半径矩形到output
            cv2.circle(img, (x, y), r, (0, 255, 0), 4)
            if idx == 0:
                four_points.append([x + r, y + r])
            elif idx == 1:
                four_points.append([x - r, y + r])
            elif idx == 2:
                four_points.append([x + r, y - r])
            elif idx == 3:
                four_points.append([x - r, y - r])
        # 根据定位圆的坐标进行透视变换
        gray_trans = four_point_transform(gray, np.array(four_points))
        img_trans = four_point_transform(img, np.array(four_points))
        # 显示新图像
        self.show_img("circle", img)
        # cv2.imshow('rect_img', img_trans)
        return gray_trans, img_trans

    # 再次根据中间横线进行透视变换
    def transform_again(self, gray_trans, img_trans):
        gaussian_bulr = cv2.GaussianBlur(gray_trans, (5, 5), 0)
        self.show_img("gaussian", gaussian_bulr)
        edged = cv2.Canny(gaussian_bulr, 75, 100)  # 边缘检测,灰度值小于2参这个值的会被丢弃，大于3参这个值会被当成边缘，在中间的部分，自动检测
        self.show_img("edged", edged)
        # 1.寻找轮廓
        image, cts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 2.将轮廓数据以{c:轮廓，peri:周长}dict形式存放到path_list里面
        path_list = []
        for c in cts:
            peri = 0.01 * cv2.arcLength(c, True)
            path_list.append({"c": c, "peri": peri})
        # 3.对集合数据根据周长进行排序
        path_sort = sorted(path_list, key=lambda x: x['peri'], reverse=True)
        # print("path_sort", path_sort)
        # 显示排序第一个的轮廓数据
        cv2.drawContours(gray_trans, [path_sort[0]['c']], -1, (0, 0, 255), 3)
        self.show_img("draw_contours", gray_trans)
        # 4.取轮廓的矩形坐标
        x, y, w, h = cv2.boundingRect(path_sort[0]['c'])
        cv2.rectangle(gray_trans, (x, y), (x + w, y + h), (0, 255, 0), 2)
        self.show_img("rectangle", gray_trans)
        # print("rect.shape()", rect.shape)
        my, mx = gray_trans.shape
        # 5.利用轮廓坐标组成新的透视定位4坐标点
        four_points = [[0, 0], [mx, 0], [0, y + h], [mx, y + h]]
        # 6.再次进行透视转换
        gray_trans2 = four_point_transform(gray_trans, np.array(four_points))
        img_trans2 = four_point_transform(img_trans, np.array(four_points))
        mhei, mwid, _ = img_trans2.shape
        print("img_trans2.shape", img_trans2.shape)  # 138, 362  204 51
        self.show_img("img_trans2", img_trans2)
        input_img = img_trans2[0:int(51 / 138 * mhei), 0:int(204 / 362 * mwid)]
        self.show_img("input_img", input_img, True)
        return input_img

    def show_img(self, title, img, wait=False):
        cv2.imshow(title, img)
        if wait:
            cv2.setMouseCallback(title, mouse_click)
            cv2.waitKey(0)

    def image_to_base64(self, image_np):
        image = cv2.imencode('.jpg', image_np)[1]
        image_code = str(base64.b64encode(image))[2:-1]
        return image_code

    def create_trackbar(self, res):
        cv2.namedWindow('tracks')
        cv2.createTrackbar("key0", "tracks", 75, 300, lambda x: None)
        cv2.createTrackbar("key1", "tracks", 200, 200, lambda x: None)
        while True:
            key0 = cv2.getTrackbarPos("key0", "tracks")
            key1 = cv2.getTrackbarPos("key1", "tracks")
            edged = cv2.Canny(res, key0, key1)  # 边缘检测,灰度值小于2参这个值的会被丢弃，大于3参这个值会被当成边缘，在中间的部分，自动检测
            self.show_img("edged", edged)
            k = cv2.waitKey(1)
            if k == 27:
                break


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("mouse_click======EVENT_LBUTTONDOWN", event, x, y)


def test_text(path="t6.png"):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang="chi_sim")
    print("pytesseract-text2==", text)


def read_text(img_base):
    try:
        cred = credential.Credential("AKIDnQq0uYw4vVoqa3GDtIRKxKQFo56rNhml", "rcASVIp54mDNHuHF0UjjTxCbkdFaeRzI")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
        req = models.GeneralHandwritingOCRRequest()
        params = {
            "ImageBase64": img_base
        }
        req.from_json_string(json.dumps(params))
        resp = client.GeneralHandwritingOCR(req)
        print("read_text========", resp.to_json_string())
        return resp.TextDetections
    except TencentCloudSDKException as err:
        print("read_text=======", err)


if __name__ == '__main__':
    answer = AnswerTest("t4.jpg")
    answer.start()
    # test_text()
