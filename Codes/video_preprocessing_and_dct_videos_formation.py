import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2,os, glob
from tqdm import tqdm

from scipy.fftpack import dct
from scipy.fftpack import idct
import numpy as np

def dct2(f):
    return dct(dct(f, axis=0, norm='ortho' ),axis=1, norm='ortho')

patch_size = 8  #8x8 patch
def  creation_dct_and_multiplicative_dct(video_path, raw_dct_path, mul_dct_path):
    img_arr = []
    dct_arr = []
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    while success:
        img_arr.append(image)
        success, image = vidcap.read()

    for r in range(64):
        I_dct = np.zeros_like(img_arr[r])
        I = img_arr[r]
        for i in range(0,I.shape[0],patch_size):
            for j in range(0,I.shape[1],patch_size):
                I_dct[i:(i+patch_size),j:(j+patch_size)] = dct2(I[i:(i+patch_size),j:(j+patch_size)])
        dct_arr.append(I_dct)
    print(np.asarray(img_arr).shape, np.asarray(dct_arr).shape)
    print('Pixel intensity range: (%d,%d)'%(dct_arr[0].min(),dct_arr[1].max()))
    
    img_arr = np.array(img_arr)
    dct_arr = np.array(dct_arr)

    out = cv2.VideoWriter(raw_dct_path,cv2.VideoWriter_fourcc(*'mp4v'), 30, (224,224))
    for j in range(64):
        print(j)
        out.write(dct_arr[j])
    out.release()
    

lists = [0,1,2]

for fi in tqdm(lists):
    video_path = "path_for_videos"
    raw_dct_path = "" #path where to store dct videos
    
    if os.path.exists(raw_dct_path):
        continue
    creation_dct_and_multiplicative_dct(video_path, raw_dct_path)
    


#Video Resize

def resize(input_file_path, output_file_path, width, height):
  os.system("ffmpeg -i {input} -vf scale={width}:{height} {output}".format(
        input=input_file_path, width=width, height=height, output=output_file_path))


files = glob.glob("location where all clips are stored")

count = 1
for f in files:
    basename = os.path.basename(f)
    input_video = f
    output_path = "path" + basename
    resize(input_file_path=input_video, output_file_path= output_path, width=224, height=224)
    print(count)
    count = count + 1












       
       
        
