from PIL import Image
from pillow_heif import register_heif_opener
import glob 
import cv2
import numpy as np 

register_heif_opener()

def image_processing(image):
    img = np.array(image)

    ### 
    height, width, _ = img.shape
    margin = 10
    img = img[margin:height-margin, margin:width-margin]
    ###

    img = cv2.resize(img, (28, 28))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv_binary = cv2.bitwise_not(binary)
    return cv_binary

def heic2image(heic_path, jpg_path): 
    image = Image.open(heic_path)
    image = image_processing(image)
    cv2.imwrite(jpg_path, image)
    return 

numbers = [number.replace('\\', '/') for number in glob.glob('DUE_MNIST/raw_data/*')]

for number in numbers: 
    n = number.split('/')[-1]
    print(f'Converting HEIC to Image with number {n}')

    jpg_path = f'DUE_MNIST/convert2image/{n}/'

    files = [file.replace('\\', '/') for file in glob.glob(f'DUE_MNIST/raw_data/{n}/*.heic')]

    for heic_path in files: 
        name_file = heic_path.split('/')[-1]
        jpg_path_cur = jpg_path+name_file.replace('heic', 'jpg')

        heic2image(heic_path, jpg_path_cur)
print('CONVERT DONE!')