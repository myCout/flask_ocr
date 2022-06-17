# -*- coding: utf-8 -*-

__author__ = 'edwin'

import sys
import os


# 冻结路径，所有路径以此为基准，打包后才能使用
def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable) #.replace("\\", "/")
    return os.path.dirname(__file__) #.replace("\\", "/")
