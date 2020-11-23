# checkbox-detection
This is a personal effort to extract checked checkbox data from PDF/image files.

Computer generated pdf: -
It uses pdfplumber python library to get details of diffrent shapes from the pdf file.
Checkes if anything is present inside given box size, if so then using re I try to extract the data.
In the data extraction segment there is a lot of scope of improvisation.

Scaned Image file: -
This file uses opencv, boxdetect, numpy and pytesseract .
Here I am reading an image using cv, changing it to gray scale, extracting checkboxes using boxdetect.
If significant amount of pixels present inside the box cosider it as checked, and if so crop out a portion from the image 
convert image to string using pytesseract OCR.
Right now lots of garbege values are comming along with the actual required value.
Trying to improvise this part.
If you have better solution please share some idea.
