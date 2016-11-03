"""
Segments a mammography image and export the area of interest (breast) to file.

Author: Thomas Schaffter (thomas.schaff...@gmail.com)
Last update: 2016-09-21
"""
import dicom
import os
import numpy as np
import sys
import cv2
#import png
from scipy.misc import imsave
from scipy.misc import bytescale

def preprocess(inImgFilename, outImgFilename):
	"""
	Identifies the location of the view position stamps on mammography images (PNG format).

	Args:
	    inImgFilename (str): path to the input mammogram in PNG format
	    outImgFilename (str): directory where the output image must be saved in PNG format
	"""
	ds = dicom.read_file(inImgFilename)
	
	# Get the laterality of the breast
	flipHorizontal = (ds.ImageLaterality == "R")

        im = bytescale(ds.pixel_array)
	img = np.copy(im)
	img2 = np.copy(im)
	height, width = img.shape[:2]

	#imgFinal = cv2.imread(inImgFilename, cv2.IMREAD_GRAYSCALE)
	imgFinal = np.copy(im)
	#imgColor = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	#ret, mask = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
    	#image_final = cv2.bitwise_and(img, img, mask = mask)
    	#ret, new_img = cv2.threshold(image_final, 180 , 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV

	textMaskColor = (255,0,255)
	paddleMaskColor = (0,255,255)
	aoiColor = (255,255,0)
	textMaskColor = paddleMaskColor = (0,0,0)

	newImg = imgFinal
	#newImg = imgColor

	paddleFound=False

	maxRect_w = 0
	maxRect_h = 0
	maxRect_x = 0
	maxRect_y = 0
	maxRect_area = 0

	# get the contours
	# cv2.findContours() modifies the input image to show only the contour	
	contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
    	for contour in contours:
        	# get the bouding box of the contour
        	[x,y,w,h] = cv2.boundingRect(contour)

        	# detect the small elements that make the image identification stamp
		if w<=2*65 and h<=65:
			cv2.rectangle(newImg,(x,y),(x+w,y+h),textMaskColor,-1)
			continue
		# detect the compression paddle
		elif w < 0.1*width and h > 0.9*height:
			cv2.rectangle(newImg,(x,y),(x+w,y+h),paddleMaskColor,-1)
			paddleFound=True
			continue
		#else:
		#	cv2.rectangle(newImg,(x,y),(x+w,y+h),aoiColor,2)

		if w*h > maxRect_area:
			maxRect_w = w
			maxRect_h = h
			maxRect_x = x
			maxRect_y = y
			maxRect_area = w*h
        	# draw rectangle around contour on original image
        	#cv2.rectangle(imgColor,(x,y),(x+w,y+h),(255,0,255),-1)
		#cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)

	# Area of interest
	#cv2.rectangle(newImg,(maxRect_x,maxRect_y),(maxRect_x+maxRect_w,maxRect_y+maxRect_h),(0,0,255),2)
	# Crop the image
	newImg = newImg[maxRect_y:maxRect_y+maxRect_h, maxRect_x:maxRect_x+maxRect_w]

	if flipHorizontal:
		#print("Flipping horizontally the image")
		newImg = cv2.flip(newImg, 1)

	cv2.imwrite(outImgFilename,newImg)
	#if (paddleFound):
#		paddleFilename = os.path.join("/paddles2/", os.path.basename(outImgFilename))
#		cv2.imwrite(paddleFilename,img2)

if __name__ == '__main__':
	inImgFilename = sys.argv[1]
        outImgFilename = sys.argv[2]

	#print("Preprocessing "+inImgFilename+" -> "+outImgFilename) ### Commented out (by syohan@au1.ibm.com) to reduce verbosity
	preprocess(inImgFilename, outImgFilename)
