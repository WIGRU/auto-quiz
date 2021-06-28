import process_image as pi
import find_cells as fc
import find_answers as fa
import time


im = './in/image.jpg'


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