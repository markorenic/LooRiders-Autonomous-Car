# import the necessary packages
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import argparse
import cv2
from finder import find_the_path, return_the_path_coordinates
from digitizer import process_image
import pygame
from queue import PriorityQueue


def find_directions(ordered_path_list):

    counter = 0
    directions = []
    heading = "east"
    print("process started")

    while(counter < len(ordered_path_list)-1):

		row1, col1 = ordered_path_list[counter]
		row2, col2 = ordered_path_list[counter+1]
		
		if heading == "east":
			if(row1 == row2):
				if(col2-col1 == 1):
					directions.append("straight-east")
					counter += 1

			elif(col1 == col2):
				if(row2-row1 == 1):
					directions.append("turn-right-to-south")
					heading = "south"

				elif(row1-row2 == 1):
					directions.append("turn-left-to-north")
					heading = "north"

		elif heading == "west":
			if(row1 == row2):
				if(col2-col1 == 1):
					directions.append("straight-west")
					counter += 1

			elif(col1 == col2):
				if(row2-row1 == 1):
					directions.append("turn-left-to-south")
					heading = "south"

				elif(row1-row2 == 1):
					directions.append("turn-right-to-north")
					heading = "north"

		elif heading == "north":
			if(col1 == col2):
				if(row2-row1 == 1):
					directions.append("straight-north")
					counter += 1

			elif(row1 == row2):

				if(col2-col1 == 1):
					directions.append("turn-right-to-east")
					heading = "east"

				elif(col1-col2 == 1):
					directions.append("turn-left-to-west")
					heading = "west"

		elif heading == "south":
			if(col1 == col2):
				if(row2-row1 == 1):
					directions.append("straight-south")
					counter += 1
			elif(row1 == row2):
				if(col2-col1 == 1):
					directions.append("turn-left-to-east")
					heading = "east"

				elif(col1-col2 == 1):
					directions.append("turn-right-to-west")
					heading = "west"


	print(directions)	



board = process_image()

find_the_path(board)

reversed_path_list = return_the_path_coordinates()

# ordered path of coordinates
ordered_path_list = reversed_path_list[::-1]

print(ordered_path_list)

find_directions(ordered_path_list)
