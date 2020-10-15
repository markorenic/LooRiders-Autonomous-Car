# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import argparse
import cv2
from finder import find_the_path, return_the_path_coordinates
import pygame
from queue import PriorityQueue

def find_puzzle(image, debug=False):
	# convert the image to grayscale and blur it slightly
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 3)
    # apply adaptive thresholding and then invert the threshold map
	thresh = cv2.adaptiveThreshold(blurred, 255,
		cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	thresh = cv2.bitwise_not(thresh)
	# check to see if we are visualizing each step of the image
	# processing pipeline (in this case, thresholding)
	"""
	if debug:
		cv2.imshow("Puzzle Thresh", thresh)
		cv2.waitKey(0)
	"""
# find contours in the thresholded image and sort them by size in
	# descending order
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	# initialize a contour that corresponds to the puzzle outline
	puzzleCnt = None
	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we can
		# assume we have found the outline of the puzzle
		if len(approx) == 4:
			puzzleCnt = approx
			break
	# if the puzzle contour is empty then our script could not find
	# the outline of the Sudoku puzzle so raise an error
	if puzzleCnt is None:
		raise Exception(("Could not find Sudoku puzzle outline. "
			"Try debugging your thresholding and contour steps."))
	# check to see if we are visualizing the outline of the detected
	# Sudoku puzzle
	"""
	if debug:
		# draw the contour of the puzzle on the image and then display
		# it to our screen for visualization/debugging purposes
		output = image.copy()
		cv2.drawContours(output, [puzzleCnt], -1, (0, 255, 0), 2)
		cv2.imshow("Puzzle Outline", output)
		cv2.waitKey(0)
	"""
    # apply a four point perspective transform to both the original
	# image and grayscale image to obtain a top-down bird's eye view
	# of the puzzle
	puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
	warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))
	# check to see if we are visualizing the perspective transform

	"""
	if debug:
		# show the output warped image (again, for debugging purposes)
		cv2.imshow("Puzzle Transform", puzzle)
		cv2.waitKey(0)
	"""

	# return a 2-tuple of puzzle in both RGB and grayscale
	return (puzzle, warped)


def is_not_empty(cell, debug=False):
	# apply automatic thresholding to the cell and then clear any
	# connected borders that touch the border of the cell
	thresh = cv2.threshold(cell, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = clear_border(thresh)

	# check to see if we are visualizing the cell thresholding step
	"""
	if debug:
		cv2.imshow("Cell Thresh", thresh)
		cv2.waitKey(0)
	"""

	# find contours in the thresholded cell
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	
	# if no contours were found than this is an empty cell(black cell)
	if len(cnts) == 0:
		return None


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
	
	if percentFilled < 0.03:
		return None

	digit = cv2.bitwise_and(thresh, thresh, mask=mask)

	# check to see if we should visualize the masking step
	if debug:
		cv2.imshow("Digit", digit)
		cv2.waitKey(0)

	# it is a white cell
	return True



image = 'sample2.jpg'
image = cv2.imread(image)
image = imutils.resize(image, width=600)

(puzzleImage, warped) = find_puzzle(image, 1)


# initialize our 9x9 sudoku board
board = np.zeros((9, 9), dtype="int")

# a sudoku puzzle is a 9x9 grid (81 individual cells), so we can
# infer the location of each cell by dividing the warped image
# into a 9x9 grid
stepX = warped.shape[1] // 9
stepY = warped.shape[0] // 9

# initialize a list to store the (x, y)-coordinates of each cell
# location
cellLocs = []

# loop over the grid locations
for y in range(0, 9):
	# initialize the current list of cell locations
	row = []

	for x in range(0, 9):
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

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
find_the_path(WIN, WIDTH, board)

reversed_path_list = return_the_path_coordinates()

#ordered path of coordinates
ordered_path_list = reversed_path_list[::-1]




def find_directions(ordered_path_list):

	counter = 0
	directions = []
	heading = "east"
	while(counter < len(ordered_path_list)-1):

		row1,col1 = ordered_path_list[counter]
		row2,col2 = ordered_path_list[counter+1]
		
		

		
		if heading == "east":
			if(row1==row2):
				if(col2-col1==1):
					directions.append("straight-east")
					print("go straight on the east route for 1 block")
					counter +=1
			elif(col1==col2):
				if(row2-row1==1):
					directions.append("turn-right-to-south")
					heading = "south"
					print("turn south")

				elif(row1-row2==1):
					directions.append("turn-left-to-north")
					heading = "north"
					print("turn north")

		elif heading == "west":
			if(row1==row2):
				if(col2-col1==1):
					directions.append("straight-west")
					print("go straight on the west route for 1 block")
					counter +=1
			elif(col1==col2):
				if(row2-row1==1):
					directions.append("turn-left-to-south")
					heading = "south"
					print("turn south")

				elif(row1-row2==1):
					directions.append("turn-right-to-north")
					heading = "north"
					print("turn north")

		elif heading == "north":
			if(col1==col2):
				if(row2-row1==1):
					directions.append("straight-north")
					print("go straight on the north route for 1 block")
					counter +=1

			elif(row1==row2):

				if(col2-col1==1):
					directions.append("turn-right-to-east")
					heading = "east"
					print("turn east")

				elif(col1-col2==1):
					directions.append("turn-left-to-west")
					heading = "west"
					print("turn west")

		elif heading == "south":
			if(col1==col2):
				if(row2-row1==1):
					directions.append("straight-south")
					print("go straight on the south route for 1 block")
					counter +=1
			elif(row1==row2):
				if(col2-col1==1):
					directions.append("turn-left-to-east")
					heading = "east"
					print("turn east")

				elif(col1-col2==1):
					directions.append("turn-right-to-west")
					heading = "west"
					print("turn west")


	print(directions)	


print(ordered_path_list)

find_directions(ordered_path_list)