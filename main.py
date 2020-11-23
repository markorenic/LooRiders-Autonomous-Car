# import the necessary packages
from digitizer import *
from finder import *
import os
from pytocs import *


board = process_image()

directions = find_the_path(board)

updatePath(directions)




