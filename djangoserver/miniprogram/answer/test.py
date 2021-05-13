# -*- coding: utf-8 -*-
import os

import cv2
import numpy as np
from imutils.perspective import four_point_transform

from answer.ocr_sdk import OcrSdk

# 在答题卡涂选答案参数
hor_space = 16  # 横向间距15
hor_que_space = 15  # 答案单个横向间距
ver_space = 26  # 纵向间距15
ver_que_space = 39  # 答案块纵向间距
# 答题卡边缘参数
start_x_margin = 2
start_y_margin = 15
# 在答题卡输入区域参数
ver_per = 51 / 138
hor_per = 204 / 362


class Answer(object):
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
        ans_list = []  # 选择的题目和答案
        gray_trans, img_trans = self.read_img()
        ans_trans, input_trans, img_trans2 = self.transform_again(gray_trans, img_trans)
        texts = self.get_input_text(input_trans)
        sel_cts = self.get_sel_point(ans_trans, img_trans2)
        card_list = self.get_card_list(ans_trans)  # 答题卡区域
        for que_item in sel_cts:
            ans_item = self.compute_score(que_item, ans_trans, card_list)
            ans_list.append(ans_item)
        print("ans_list", ans_list)
        return ans_list, texts, self.points_file_name, self.file_name

    # 读取图片，根据四个定位圆进行透视变换
    def read_img(self):
        # 载入并显示图片
        print("self.path==============", self.path)
        img = cv2.imread(self.path)
        wid, hei, _ = img.shape
        img = cv2.resize(img, (int(hei / 2), int(wid / 2)), 0, 0)
        # img = cv2.resize(img, (500, 700), 0, 0)
        self.show_img("img", img)
        # 1.降噪（模糊处理用来减少瑕疵点）
        result = cv2.blur(img, (5, 5))
        # 2.灰度化,就是去色（类似老式照片）
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # 3.霍夫变换圆检测-定位答题卡圆圈位置
        circles = cv2.HoughCircles(gray.copy(), cv2.HOUGH_GRADIENT, 1, 200, param1=250, param2=15, minRadius=5,
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
        ans_four_points = [[0, y + h], [mx, y + h], [0, my], [mx, my]]  # 答案定位四点
        input_four_points = [[0, 0], [mx, 0], [0, y + h], [mx, y + h]]  # 输入框定位四点
        # 6.再次进行透视转换
        ans_trans = four_point_transform(gray_trans, np.array(ans_four_points))
        img_trans2 = four_point_transform(img_trans, np.array(ans_four_points))
        input_trans = four_point_transform(img_trans, np.array(input_four_points))
        return ans_trans, input_trans, img_trans2

    # 获取输入的文字
    def get_input_text(self, img_trans2):
        self.show_img("get_input_text", img_trans2)
        mhei, mwid, _ = img_trans2.shape
        print("img_trans2.shape", img_trans2.shape)  # 138, 362  204 51
        # 裁剪输入图片
        input_img = img_trans2[0:int(ver_per * mhei), 0:int(hor_per * mwid)]
        self.show_img("input_img", input_img)
        ocr = OcrSdk()
        texts = ocr.read_text_cv(input_img)
        return texts

    # 获取选中的答案
    def get_sel_point(self, gray_trans2, img_trans2):
        self.show_img("get_sel_point", gray_trans2)
        thresh2 = cv2.adaptiveThreshold(gray_trans2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 17, 25)
        self.show_img("ostu2", thresh2)
        r_image, r_cnt, r_hierarchy = cv2.findContours(thresh2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print("找到轮廓个数----------------：", len(r_cnt))
        # 使用红色标记所有的轮廓
        cv2.drawContours(img_trans2, r_cnt, -1, (0, 0, 255), 2)
        # 把所有找到的轮廓，给标记出来
        sel_cts = []
        for cxx in r_cnt:
            # 通过矩形，标记每一个指定的轮廓
            x, y, w, h = cv2.boundingRect(cxx)
            ar = w / float(h)
            if (w >= 9 or h >= 5) and w < 20:
                cv2.rectangle(img_trans2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # 把每个选项，保存下来
                sel_cts.append([x, y, w, h])
        self.show_img("sel_point", img_trans2)
        print("sel_cts========", len(sel_cts))
        cv2.imwrite(self.points_path, img_trans2)
        return sel_cts

    # 计算分数
    def compute_score(self, que_item, img_trans2, card_list):
        # print("que=========", que_item)
        x, y, w, h = que_item
        cx = x + w / 2  # 中心x坐标
        cy = y + h / 2  # 中心y坐标
        # 便于调试，显示当前题目及答案
        cv2.rectangle(img_trans2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        choose_que = []
        for coo in card_list:
            x, y = coo['value']
            # print("coo", x, y)
            if x + hor_que_space > cx > x and y + ver_que_space > cy > y:
                choose_ans = self.get_answer(cy - y, ver_que_space)
                # print("题目{},答案{}".format(coo['key'], choose_ans))
                choose_que = [coo['key'], choose_ans]
                break
        # print("choose_que", choose_que)
        # self.show_img("ox_1", img_trans2, True)
        return choose_que

    @staticmethod
    def get_card_list(ans_trans):
        card_list = []
        for j in range(5):
            for i in range(20):
                hor_space_num = i // 5 + 1  # 所在横向块数
                hor_piece_num = (i + 1) % 5  # 所在横向份数
                start_x = (hor_space_num - 1) * hor_space + hor_que_space * i + start_x_margin
                # if i == 0 and j == 0:
                    # print("横向的第{}块，第{}份，起始x坐标{}".format(hor_space_num, hor_piece_num, start_x))  # 横向的第几块，第几份
                start_y = (ver_space + ver_que_space) * j + start_y_margin
                # if i == 0 and j == 2:
                #     print("纵向的第{}块，起始y坐标{}".format(j + 1, start_y))  # 纵向的第几块，第几份
                card_list.append({"key": j * 20 + (i + 1), "value": [start_x, start_y]})
        # print("ans_shape", ans_trans.shape)  # h:317 w:345
        # print("card_list", card_list)
        # cv2.setMouseCallback("sel_point", mouse_click)
        # cv2.waitKey(0)
        return card_list

    # 获取答案
    def get_answer(self, sel, all):
        percent = sel / all
        if percent < 1 / 5:
            return "num"
        elif percent < 2 / 5:
            return "A"
        elif percent < 3 / 5:
            return "B"
        elif percent < 4 / 5:
            return "C"
        elif percent < 1:
            return "D"

    def show_img(self, title, img, wait=False):
        cv2.imshow(title, img)
        if wait:
            cv2.setMouseCallback(title, mouse_click)
            cv2.waitKey(0)


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("mouse_click======EVENT_LBUTTONDOWN", event, x, y)


if __name__ == '__main__':
    answer = Answer("../../media/images/mini_t7.jpg")
    answer.start()
