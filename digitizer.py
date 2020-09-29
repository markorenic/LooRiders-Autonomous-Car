# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import argparse
import cv2
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
	if debug:
		cv2.imshow("Puzzle Thresh", thresh)
		cv2.waitKey(0)
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
	if debug:
		# draw the contour of the puzzle on the image and then display
		# it to our screen for visualization/debugging purposes
		output = image.copy()
		cv2.drawContours(output, [puzzleCnt], -1, (0, 255, 0), 2)
		cv2.imshow("Puzzle Outline", output)
		cv2.waitKey(0)
    	# apply a four point perspective transform to both the original
	# image and grayscale image to obtain a top-down bird's eye view
	# of the puzzle
	puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
	warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))
	# check to see if we are visualizing the perspective transform
	if debug:
		# show the output warped image (again, for debugging purposes)
		cv2.imshow("Puzzle Transform", puzzle)
		cv2.waitKey(0)
	# return a 2-tuple of puzzle in both RGB and grayscale
	return (puzzle, warped)


def is_empty(cell, debug=True):
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

	# if no contours were found than this is an empty cell
	if len(cnts) == 0:
		return True
	else:
		return False



image = 'sudoku_puzzle.jpg'
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
		digit = is_empty(cell, 0)

		# verify that the digit is not empty
		if digit == False:
			board[y, x] = 1
		else:
			board[y, x] = 0
	# add the row to our cell locations
	cellLocs.append(row)
print(board)