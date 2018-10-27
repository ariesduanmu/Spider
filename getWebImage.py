import os
import requests
import threading
import time
from queue import Queue
from PIL import Image
import io

from itertools import product

def image_save_path(img_save_dir, img_name):
    return os.path.abspath(os.path.join(img_save_dir, img_name))

def image_url(point, d, level, row, col):
    return f"http://www.wsxflszlclg.com/xfclg/panos/pano_{point:02}.tiles/{d}/{level}/0{row}/{image_name(level, d, row, col)}"

def image_name(level, d, row, col):
    return f"{level}_{d}_{row:02}_{col:02}.jpg"

def request_download(img_url):
    r = requests.get(img_url)
    if r.status_code == 200:
        return Image.open(io.BytesIO(r.content))
    return None

def crawl_image(save_path, d, point, level, row_num, col_num, last_width, last_height, normal):
    to_img = Image.new('RGB', (normal*(row_num-1)+last_width, normal*(col_num-1)+last_height))
    for k in range(row_num*col_num):
        row = k // row_num
        col = k % row_num
        img_url = image_url(point, d, level, row+1, col+1)
        image = request_download(img_url)
        if image is not None:
            to_img.paste(image, (col*normal,row*normal))
    to_img.save(image_save_path(save_path, f"{point:02}_{d}.jpg"))

def crawl_mulitithread(save_path, points, level, row_num, col_num, last_width, last_height, normal=512):
    start = time.time()
    for d, point in product('bdfulr', range(1,points+1)):
        t = threading.Thread(target=crawl_image, args=(save_path, d, point, level, row_num, col_num, last_width, last_height, normal))
        t.start()
    print(f"Multithread Spend: {time.time()-start}")

def crawl_without_mulitithread(save_path, points, level, row_num, col_num, last_width, last_height, normal=512):
    start = time.time()
    for d, point in product('bdfulr', range(1,points+1)):
        crawl_image(save_path, d, point, level, row_num, col_num, last_width, last_height, normal)
    print(f"Single Spend: {time.time()-start}")

def main():
    save_paths = ['image_l1','image_l2','image_l3','test']
    levels = ['l1','l2','l3','l1']
    row_nums = [3,5,9,1]
    col_nums = [3,5,9,1]
    last_widths = [128,128,256,128]
    last_heights = [128,128,256,128]
    points = 36

    for i in range(1):
        save_path = save_paths[i]
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        level = levels[i]
        row_num = row_nums[i]
        col_num = col_nums[i]
        last_width = last_widths[i]
        last_height = last_heights[i]
        crawl_mulitithread(save_path, points, level, row_num, col_num, last_width, last_height)
        os.remove(save_path)
        os.mkdir(save_path)
        crawl_without_mulitithread(save_path, points, level, row_num, col_num, last_width, last_height)

if __name__ == '__main__':
    main()
