import process_image as pi
import find_cells as fc
import find_answers as fa

import time
import configparser
import os

im = './in/image.jpg'

def process(im):
    config = configparser.ConfigParser()
    config.read('./src/settings.ini')
    default = config['DEFAULT']
    out_path = default['out_path']

    # if out folder doesn't exist, make folder
    if not os.path.isdir(out_path):
        os.mkdir(out_path)



    start_time = time.perf_counter()

    con = pi.process(im)

    finish_time = time.perf_counter()
    duration = finish_time - start_time
    print(f'process image, duration: { duration }')


    start_time = time.perf_counter()

    cel = fc.find(con['contours'], con['image'])

    finish_time = time.perf_counter()
    duration = finish_time - start_time
    print(f'find cells, duration: { duration }')

    start_time = time.perf_counter()

    res = fa.find(cel['cells'], im, con['image'])

    finish_time = time.perf_counter()
    duration = finish_time - start_time
    print(f'find answers, duration: { duration }')

    print(f'correct answers: {res["corr"]}')

    return res["corr"]

if __name__ == '__main__':
    process(im)