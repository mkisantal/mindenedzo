import unittest
import numpy as np

import extract

class TestLoad(unittest.TestCase):
    def test_load(self):
        test_image_path = './test_images/ScreenShot_19-02-07_16-29-44-000.jpg'
#         test_image_path = 'ScreenShot_19-02-07_16-29-44-000.jpg'
        self.assertIsInstance(extract.load(test_image_path), np.ndarray)
        
class TestExtractCrops(unittest.TestCase):
    
    def test_extract_crops(self):
        dummy_np_image = np.zeros([1080, 1920, 3], dtype=np.uint8)
        crops = extract.extract_crops(dummy_np_image)
        self.assertIsInstance(crops, dict)
        self.assertEqual(len(crops), 6)
        valid_keys = set(['eliminations', 'kills', 'time',
                          'damage', 'healing', 'deaths'])
        for key in crops.keys():
            self.assertTrue(key in valid_keys)
            self.assertIsInstance(crops[key], np.ndarray)
            self.assertTrue(crops[key].size > 100)
            
class TestOcr(unittest.TestCase):
    
    def test_ocr(self):
        dummy_char_one = np.zeros([20, 20, 3], dtype=np.uint8)
        dummy_char_one[2:18, 8:12, :] = 255
        
        valid_keys = set(['eliminations', 'kills', 'time',
                          'damage', 'healing', 'deaths'])
        dummy_crop_dict = {key: dummy_char_one for key in valid_keys}
        results = extract.ocr(dummy_crop_dict)
        
        self.assertIsInstance(results, dict)
        for key in valid_keys:
            res = results[key]
            self.assertIsInstance(res, str)
    
    
class IntegrationTest(unittest.TestCase):
    
    def test_integration(self):
        test_images = ['./test_images/ScreenShot_19-02-07_16-29-44-000.jpg',
                       './test_images/ScreenShot_19-02-07_16-30-03-000.jpg',
                       './test_images/ScreenShot_19-02-07_16-30-10-000.jpg']

        results = []
        for test_image_path in test_images:
            np_img = extract.load(test_image_path)
            crops = extract.extract_crops(np_img)
            results.append(extract.ocr(crops))

        ground_truths = []
        ground_truths.append({'eliminations': '2',
                              'kills': '2',
                              'time': '00:05',
                              'damage': '535',
                              'healing': '0',
                              'deaths': '0'})
        ground_truths.append({'eliminations': '4',
                              'kills': '4',
                              'time': '00:16',
                              'damage': '1,730',
                              'healing': '0',
                              'deaths': '0'})
        ground_truths.append({'eliminations': '5',
                              'kills': '5',
                              'time': '00:23',
                              'damage': '1,825',
                              'healing': '0',
                              'deaths': '0'})
            
        for result, ground_truth in zip(results, ground_truths):
            for key in result.keys():
                self.assertEqual(result[key], ground_truth[key])
            
    
if __name__ == '__main__':
    unittest.main()