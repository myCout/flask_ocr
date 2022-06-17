# -*- coding: utf-8 -*-
# @Time : 2022/4/26 17:55
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : BaiDuOcr.py
# @Project : src


from paddleocr import PaddleOCR
import frozen_dir
import os, time
import cv2

"""
class Singleton中的__init__在Myclass声明的时候被执行Myclass=Singleton()
Myclass()执行时，最先执行父类的__call__方法（object,Singleton都作为Myclass的父类，
根据深度优先算法，会执行Singleton中的__call__()，Singleton中的__call__()写了单例模式）
"""


class Singleton(type):

    def __init__(self, name, bases, dict):
        super(Singleton, self).__init__(name, bases, dict)
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(Singleton, self).__call__(*args, **kwargs)
        return self._instance


class BaiDuOcr(object, metaclass=Singleton):

    def __init__(self, det_path, rec_path):
        # root_path = frozen_dir.app_path()
        #
        # if os.path.exists(det_path):
        #     print("YYY")
        #     # 绝对路径
        #     self.det_file_path = det_path
        # else:
        #     print("NNN")
        #     # 相对路径
        #     self.det_file_path = root_path + '/' + det_path
        #
        # if os.path.exists(rec_path):
        #     # 绝对路径
        #     self.rec_file_path = rec_path
        # else:
        #     # 相对路径
        #     self.rec_file_path = root_path + '/' + rec_path
        self.det_file_path = det_path
        self.rec_file_path = rec_path
        self._config_orc()

    def _config_orc(self):
        self.baidu_ocr = PaddleOCR(det_model_dir=self.det_file_path,
                                   rec_model_dir=self.rec_file_path,
                                   use_angle_cls=True,
                                   lang="ch",
                                   show_log=False,
                                   use_gpu=False)

    def image_ocr(self, target_image, gray_mode=True):
        if gray_mode:
            gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)  ##要二值化图像，必须先将图像转为灰度图
            ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # 自定义阈值
        else:
            binary = target_image
        result = self.baidu_ocr.ocr(binary, det=True, cls=True)
        if result is None:
            return None

        for line in result:
            confidence = line[1][1]
            if confidence >= 0.6:
                result_str = line[1][0]
                return result_str.strip()
            else:
                return None
