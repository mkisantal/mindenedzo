# Text processing from still images

This repository contains a solutin for the [e-sport startup] technical assignment. Probably not the best possible solution as I didn't end up hired. The task is to extract textual information from still images.

  - The solution code is in `extract.py`
  - Corresponding unit and integration tests in `test.py`
  - Processing results in the `results/` folder
  
 ### Installation
 
 The solution relies PIL for image loading, and on Tesseract for OCR. this software and its python bindings has to be installed.
 ```
 sudo apt install tesseract-ocr
 pip install pytesseract
 pip install pillow
 ```
 
### Running the solution and tests
Solution:
```
python extract.py --verbose -i [path/to/image/dir]
```
Tests:
```
python test.py
```
