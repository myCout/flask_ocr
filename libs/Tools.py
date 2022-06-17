import base64
import hashlib
import os
import platform
import random
import re
import string
import sys
import time
import frozen_dir
# import rsa

# platform_name = platform.system()
# if platform_name == "Windows":
#     import win32api
# elif platform_name == "Linux":
#     pass
#
# from PIL import ImageDraw


class Tools(object):
    @staticmethod
    def get_os_split():
        if platform.system() == "Windows":
            return '\\'
        else:
            return '/'

    @staticmethod
    def get_os_path(path):
        if platform.system() == "Windows":
            return path.replace("/", "\\")
        else:
            return path.replace("\\", "/")

    @staticmethod
    def os_path_join(parrent_path, sub_path):
        path = Tools.get_os_path(os.path.join(parrent_path, sub_path))
        return path

    @staticmethod
    def get_abs_path(relative_path):
        return Tools.os_path_join(frozen_dir.app_path(), relative_path)

    @staticmethod
    def get_app_path():
        return frozen_dir.app_path()

    @staticmethod
    def get_runtime_path():
        '''返回运行绝对路径。'''
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller会创建临时文件夹temp
            # 并把路径存储在_MEIPASS中
            runtime_path = sys._MEIPASS
        else:
            runtime_path = frozen_dir.app_path()
        return runtime_path

    @staticmethod
    def resource_path(relative_path=None):
        '''返回资源绝对路径。'''
        return Tools.get_os_path(os.path.join(Tools.get_runtime_path(), relative_path))

    @staticmethod
    def mkfile(path, content=None):
        try:
            f = open(path, "w", encoding='utf-8')  # 打开文件
            # f.seek(0)
            # f.truncate()
            if content:
                f.write(content)
            f.close()
        except Exception as err:
            print('Tools->mkfile(%r) except:' % path, err)
            return False
        return True

    @staticmethod
    def mkdir(path):
        # 引入模块
        import os
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \(windows)或/(unix) 符号
        path = path.rstrip(Tools.get_os_split())
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            try:
                os.makedirs(path)
                # print(path + ' 创建成功')
            except Exception as err:
                # print('创建失败: {}'.format(err))
                return False
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print(path + ' 目录已存在')
            return False

    # 字典按键排序
    @staticmethod
    def dict_sort_by_key(d):
        # sorted(d.keys()) 返回重新排序的列表
        new_d = {}
        for i in sorted(d.keys()):
            new_d[i] = d[i]
        return new_d

    # 测试函数运行时间
    @staticmethod
    def cal_time(fn):
        """计算性能的修饰器"""

        def wrapper(*args, **kwargs):
            starTime = time.time()
            f = fn(*args, **kwargs)
            endTime = time.time()
            # print('%s() runtime:%s ms' % (fn.__name__, 1000 * (endTime - starTime)))
            print('%s() runtime:%s s' % (fn.__name__, (endTime - starTime)))
            return f

        return wrapper

    @staticmethod
    # 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
    def getPixel(image, x, y, G, N):
        L = image.getpixel((x, y))
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0
        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if (nearDots < N) and (L == False):
            return image.getpixel((x, y - 1))
        else:
            return None

    # 降噪
    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
    # G: Integer 图像二值化阀值
    # N: Integer 降噪率 0 <N <8
    # Z: Integer 降噪次数
    # 输出
    #  0：降噪成功
    #  1：降噪失败
    @staticmethod
    def clearNoise(image, G, N, Z):
        draw = ImageDraw.Draw(image)

        for i in range(0, Z):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    color = Tools.getPixel(image, x, y, G, N)
                    if color != None:
                        draw.point((x, y), color)

    @staticmethod
    def random_chinese(num=1, black_list="中操傻共产党法轮功逼国家领导性色妈爸爷孙日"):
        result = ""
        while len(result) < num:
            cn_char = chr(random.randint(0x4E00, 0x9FA5))
            if (cn_char in black_list):
                continue
            result += cn_char
        return result

    @staticmethod
    def random_letter(num=1, black_list=""):
        result = ""
        while len(result) < num:
            # s = string.ascii_letters
            s = string.ascii_uppercase
            r = random.choice(s)
            if r in black_list:
                continue
            result += r
        return result

    @staticmethod
    def interval_do(interval, duration, func, *parameters):
        start_time = time.time()
        # print('XXX start_time:', start_time, duration, interval)
        while True:
            find_start_time = time.time()
            result = func(*parameters)
            find_end_time = time.time()
            if result is not None:
                # 获得结果
                break
            if (find_end_time - start_time) >= duration:
                # 超时退出
                # print('XXX expire_time:', find_end_time - start_time, duration)
                break
            sleep_time = interval - (find_end_time - find_start_time)
            if sleep_time > 0:
                # print('XXX sleep_time:', sleep_time)
                time.sleep(sleep_time)
        # print('XXX end_time:', time.time() - start_time)
        return result
