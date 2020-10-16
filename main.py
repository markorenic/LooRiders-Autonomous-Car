# import the necessary packages
from digitizer import *
from finder import *
import os


#send instrustions array
def updatePath(instructions):
    file_ = open("firmware/firmware.ino", "r")
    message = ""
    for row in file_:
        if ("loop()" not in row):
            #print(row)
            message = message + row
        else:
            break
    file_.close()

    file_ = open("firmware/firmware.ino", "w")
    message = message + "void loop(){"

    #instructions
    instructions_code = ""
    for instruction in instructions:
        if instruction == "left":
            instructions_code = instructions_code + " NinetyLeft();"
        if instruction == "right":
            instructions_code = instructions_code + " NinetyRight();"        
        if instruction == "forward":
            instructions_code = instructions_code + " OneSpaceForward();"

    message  = message + instructions_code + " while(1); return;}"
    file_.write(message)
    file_.close()


board = process_image()

directions = find_the_path(board)

print(directions)

updatePath(directions)



