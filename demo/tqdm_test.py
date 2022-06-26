from tqdm import tqdm
from time import sleep

bar = tqdm(['p1','p2','p3','p4','p5'])
for b in bar:
    sleep(0.1)
    bar.set_description("处理{0}中".format(b))
    