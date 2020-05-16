import pytesseract
import os
import numpy as np
from PIL import Image
import csv
import argparse

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

        if key == 'damage':  # removing commas
            ocr_result = ocr_result.replace(',', '')

        ocr_results[key] = ocr_result
    return ocr_results
   
    
def print_results(ocr_results):
    for key in TARGETS:
        print('{}: {}'.format(key, ocr_results[key]))
    print('--'*5)
    return


def write_results(ocr_results, img_name):
    if img_name.endswith('.jpg'):
        img_name = img_name[:-4]
    out_path = 'result_{}.csv'.format(img_name)
    with open(out_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for key in ocr_results.keys():
            csv_writer.writerow([key, str(ocr_results[key])])
    return


def load(img_path):
    pil_img = Image.open(img_path)
    np_img = np.array(pil_img)
    return np_img
             
             
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--img_dir', type=str,
                        default='/home/ubuntu/data/Screenshots/',
                        help="directory of images to be processedd")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="shows output", default=False)
    args = parser.parse_args()

    img_name_list = [img for img in sorted(os.listdir(args.img_dir))
                     if img.endswith('.jpg')]

    print('Processing started. 🚀')
    for img_name in img_name_list:
        print(img_name)
        img_path = os.path.join(args.img_dir, img_name)
        np_img = load(img_path)
        crops = extract_crops(np_img)
        results = ocr(crops)
        if args.verbose:
            print_results(results)
        write_results(results, img_name)
    print('Processing done. ✅')

if __name__ == '__main__':
    main()

              
    
    
