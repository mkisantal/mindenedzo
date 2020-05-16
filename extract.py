import pytesseract
import os
import numpy as np
from PIL import Image


# path and names
img_dir = '/home/ubuntu/data/Screenshots/'
img_name_list = sorted(os.listdir(img_dir))
example_name = img_name_list[-1]
img_name_list = img_name_list[:-1]

TARGETS = ['eliminations', 'kills', 'time', 'damage', 'healing', 'deaths']
tesseract_config = '--psm 7 --oem 0 -c tessedit_char_whitelist=0123456789,:'


def extract_crops(np_img):
    
    crop_dict = dict()
    crop_dict['eliminations'] = np_img[890:920, 132:157]  # eliminations
    crop_dict['kills'] = np_img[890:920, 382:406]  # objective kills
    crop_dict['time'] = np_img[890:920, 625:700]  # objective time
    crop_dict['damage'] = np_img[955:980, 130:205]  # damage done
    crop_dict['healing'] = np_img[955:980, 380:405]  # healing done
    crop_dict['deaths'] = np_img[955:980, 632:654]  # deaths 
    return crop_dict


def ocr(crop_dict):
    ocr_results = dict()
    for key in TARGETS:
        ocr_result = pytesseract.image_to_string(crop_dict[key],
                                                 config=tesseract_config)
        if ocr_result == '':
            crop = np.hstack([crop_dict[key], crop_dict[key], crop_dict[key]])
            ocr_result = pytesseract.image_to_string(crop, config=tesseract_config)
            if len(ocr_result) > 2:
                ocr_result = ocr_result[len(ocr_result)//3]
            else:
                ocr_result = '1'
        ocr_results[key] = ocr_result
    return ocr_results
   
    
def print_results(ocr_results):
    for key in TARGETS:
        print('{}: {}'.format(key, ocr_results[key]))
    print('--'*5)
    return


def load(img_path):
    pil_img = Image.open(img_path)
    np_img = np.array(pil_img)
    return np_img
             
             
def main():
    print('started')
    for img_name in img_name_list:
        print(img_name)
        img_path = os.path.join(img_dir, img_name)
        np_img = load(img_path)
        crops = extract_crops(np_img)
        results = ocr(crops)
        print_results(results)


if __name__ == '__main__':
    main()

              
    
    
