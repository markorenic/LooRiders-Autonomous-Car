# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import argparse
import cv2
import pygame
from queue import PriorityQueue

def find_map(image, debug=False):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert the image to grayscale and blur it slightly
	blurred = cv2.GaussianBlur(gray, (7, 7), 3)    # apply adaptive thresholding and then invert the threshold map
	thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	thresh = cv2.bitwise_not(thresh)
	if debug:
		cv2.imshow("map Thresh", thresh)
		cv2.waitKey(0)
    # find contours in the thresholded image and sort them by size in descending order
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	
	mapCnt = None #contours for the map outline

	for c in cnts: # loop over the contours
		
		peri = cv2.arcLength(c, True) # approximate the contour
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we can
		# assume we have found the outline of the map
		if len(approx) == 4:
			mapCnt = approx
			break
	# if the map contour is empty then our script could not find
	# the outline of the  map so raise an error
	if mapCnt is None:
		raise Exception(("Could not find  map outline. "
			"Try debugging your thresholding and contour steps."))
	# check to see if we are visualizing the outline of the detected
	#  map
	if debug:
		# draw the contour of the map on the image and then display
		# it to our screen for visualization/debugging purposes
		output = image.copy()
		cv2.drawContours(output, [mapCnt], -1, (0, 255, 0), 2)
		cv2.imshow("map Outline", output)
		cv2.waitKey(0)
    # apply a four point perspective transform to both the original
	# image and grayscale image to obtain a top-down bird's eye view
	# of the map
	map = four_point_transform(image, mapCnt.reshape(4, 2))
	warped = four_point_transform(gray, mapCnt.reshape(4, 2))
	# check to see if we are visualizing the perspective transform

	if debug:
		# show the output warped image (again, for debugging purposes)
		cv2.imshow("map Transform", map)
		cv2.waitKey(0)

	# return a 2-tuple of map in both RGB and grayscale
	return (map, warped)


def is_not_empty(cell, debug=False):
	# apply automatic thresholding to the cell and then clear any
	# connected borders that touch the border of the cell
	thresh = cv2.threshold(cell, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = clear_border(thresh)

	# check to see if we are visualizing the cell thresholding step
	if debug:
		cv2.imshow("Cell Thresh", thresh)
		cv2.waitKey(0)

	# find contours in the thresholded cell
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	
	# if no contours were found than this is an empty cell(black cell)
	if not (len(cnts) == 0):
		# otherwise, find the largest contour in the cell and create a
		# mask for the contour
		c = max(cnts, key=cv2.contourArea)
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)


		# compute the percentage of masked pixels relative to the total
		# area of the image
		(h, w) = thresh.shape
		percentFilled = cv2.countNonZero(mask) / float(w * h)

		# if less than 3% of the mask is filled then we are looking at
		# noise and can safely ignore the contour
		# it is a black cell
		
		if percentFilled > 0.02:
			return True

		digit = cv2.bitwise_and(thresh, thresh, mask=mask)

		# check to see if we should visualize the masking step
		if debug:
			cv2.imshow("Digit", digit)
			cv2.waitKey(0)

	# it is a white cell
	return None


def process_image():

	image = 'actual_pic.jpg'
	image = cv2.imread(image)
	image = imutils.resize(image, width=600)

	(mapImage, warped) = find_map(image, 0)


	# initialize our 9x9  board
	board = np.zeros((6, 6), dtype="int")

	# a  map is a 9x9 grid (81 individual cells), so we can
	# infer the location of each cell by dividing the warped image
	# into a 9x9 grid
	stepX = warped.shape[1] // 6
	stepY = warped.shape[0] // 6

	# initialize a list to store the (x, y)-coordinates of each cell
	# location
	cellLocs = []

	# loop over the grid locations
	for y in range(0, 6):
		# initialize the current list of cell locations
		row = []

		for x in range(0, 6):
			# compute the starting and ending (x, y)-coordinates of the
			# current cell
			startX = x * stepX
			startY = y * stepY
			endX = (x + 1) * stepX
			endY = (y + 1) * stepY

			# add the (x, y)-coordinates to our cell locations list
			row.append((startX, startY, endX, endY))

			# crop the cell from the warped transform image and then
			# extract the digit from the cell
			cell = warped[startY:endY, startX:endX]
			digit = is_not_empty(cell, False)

			if digit == None:
				board[x,y]=0
			
			elif digit == True:

				board[x,y]=1
				
				
		# add the row to our cell locations
		cellLocs.append(row)

	return board



