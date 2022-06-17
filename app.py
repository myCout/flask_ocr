# -*- coding:utf-8 -*-

from flask import Flask
import time

from flask import Flask, request, jsonify
from libs.Tools import Tools
from libs.BaiDuOcr import BaiDuOcr
import base64
import cv2 as cv
import numpy as np

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello OCR!'


@app.route("/ocr", methods=['POST', 'GET'])
def zh_ocr():
    # 解析图片数据
    img = base64.b64decode(str(request.form['image']))
    image_data = np.fromstring(img, np.uint8)
    image_data = cv.imdecode(image_data, cv.IMREAD_COLOR)
    # cv.imshow("output", image_data)
    # cv.waitKey(0)
    # cv.imwrite("./ppocr_img/game/result{}.png".format(time.time()), image_data)
    result = baidu_ocr("mhxy_train/mhxy_train_det", "mhxy_train/mhxy_train_rec", image_data, False)
    obj = {
        "status": 200,
        "content": result
    }
    print(obj)
    return jsonify(obj)


@app.route("/baiduocr", methods=['POST', 'GET'])
def image_ocr():
    imgfile = request.files['file']
    imgfile = np.asarray(bytearray(imgfile.read()), dtype="uint8")
    image_data = cv.imdecode(imgfile, cv.IMREAD_COLOR)
    result = baidu_ocr("mh_train/mhxy_train_det", "mh_train/mhxy_train_rec", image_data, False)
    print(result)
    obj = {
        "status": 200,
        "content": result
    }
    # print(result)
    return jsonify(obj)


def baidu_ocr(det_path=None, rec_path=None, source=None, gray_mode=True):
    base_path = Tools.get_abs_path('weight/')
    bd_ocr = BaiDuOcr(base_path + det_path, base_path + rec_path)
    result = bd_ocr.image_ocr(source, gray_mode)
    return result


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=9000)
