"""本模块用于实现图片到字符画的转换"""
from tkinter import *
from tkinter.messagebox import *

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def convert(import_img: str, input_char: str, pix_distance: str):
    """
    字符画转换函数
    import_img是原图像的路径
    input_char是字符画的字符列表
    pix_distance是像素距离，用于控制图片清晰度
    """
    scale = 1  # 缩放比例
    default_char = "!@#$%^&*QWRTUIJBHvnloambOJNkmggMKH"  # 默认组成字符画的字符
    img = Image.open(import_img)
    img_pix = img.load()
    img_width = img.size[0]
    img_height = img.size[1]
    canvas_array = np.ndarray((img_height * scale, img_width * scale, 3), np.uint8)
    canvas_array[:, :, :] = 255
    new_img = Image.fromarray(canvas_array)
    img_draw = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("simsun.ttc", 10)

    if input_char == "(默认)":
        char_list = list(default_char)
    else:
        char_list = list(input_char)

    pix_distance_ = 0

    if pix_distance == "清晰":
        pix_distance_ = 3
    elif pix_distance == "一般":
        pix_distance_ = 4
    elif pix_distance == "字符":
        pix_distance_ = 5
    else:
        showerror("错误", "无法识别您输入的清晰度，请重试")

    pix_count = 0
    table_len = len(char_list)
    for y in range(img_height):
        for x in range(img_width):
            if x % pix_distance_ == 0 and y % pix_distance_ == 0:
                img_draw.text((x * scale, y * scale), char_list[pix_count % table_len],
                              img_pix[x, y], font)
                pix_count += 1

    return new_img
