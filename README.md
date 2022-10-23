# MakeUC-2022
MakeUC 22 Hackathon Submission - Saaras Pakanati

## Introduction
The code was created for submitting to the MakeUC 22 Hackathon. It prompts the user to provide an image of any FDA Drug Label and reads the information provided on it. Its current functionality looks for a few key words and expiry data. Based on that information, it makes a google calander to throw away the medication.

## Software and languages used
The base code has been coded on Python along with the use of the following libraries and services:

1. OpenCV (cv2)
  https://pypi.org/project/opencv-python/
  
2. Google Tesseract (pytesseract)
  https://pypi.org/project/pytesseract/
  In additon to the package, the following link goes through the additional downloads required to execute the code.
  https://github.com/tesseract-ocr/tesseract
  
3. Numpy (numpy)
  https://numpy.org/
  
4. Google Calendar API
    https://developers.google.com/calendar/api/concepts
    
## References
1. Anand Jagadeesan (https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/) 
  - For detection of information of data in the image section of the code.
  - Additions made by me inslcude thresholding the images to comply with the 
        the LEGO instruction sheets in a more efficient and accurate manner.
        
2. https://pypi.org/project/opencv-python/

3. https://pypi.org/project/pytesseract/
 
4. https://github.com/tesseract-ocr/tesseract

5. https://numpy.org/

6. https://developers.google.com/calendar/api/concepts


## Conclusion
This code has been optimized for reading the FDA Drug Labels. For any wider application, play around with the thresholding of the image. 
