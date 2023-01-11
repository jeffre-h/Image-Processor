# Description: The definition of the functions that are used to manipulate the image

import display
import numpy

# inverts the pixels
def invert(pixels, editedImg):
    width = len(pixels)
    height = len(pixels[0])

    # loop through each pixel in the image
    # change the rgb values of each pixel to 255 - the original value (inverts)
    for row in range(width):
        for column in range(height):
            pixel = pixels[row][column]
            r = 255 - pixel[0]
            g = 255 - pixel[1]
            b = 255 - pixel[2]
            editedImg[row][column] = [r,g,b]
    
    return editedImg

# flips the image horizontally
def flipHorizontal(pixels, editedImg):
    width = len(pixels)
    height = len(pixels[0])
    lastColumn = width - 1

    # loop through each pixel in the image
    # swap the column positions so that it flips horizontally
    for row in range(width):
        for column in range(height):
            newColumn = lastColumn - row
            editedImg[row][column] = pixels[newColumn][column]

    return editedImg

# flips the image vertically
def flipVertical(pixels, editedImg):
    width = len(pixels)
    height = len(pixels[0])
    lastColumn = height - 1

    # loop through each pixel in the image
    # swap the row positions so that it flips vertically
    for row in range(width):
        for column in range(height):
            newColumn = lastColumn - column
            editedImg[row][column] = pixels[row][newColumn]
        
    return editedImg

# removes the red, green, or blue channel in the image.
def remove_color(pixels, color, editedImg):
    width = len(pixels)
    height = len(pixels[0])

    for row in range(width):
        for column in range(height):
            pixel = pixels[row][column]
            # changing either the r, g, or b value to 0
            if color == "red":
                pixel[0] = 0
            elif color == "green":
                pixel[1] = 0
            elif color == "blue":
                pixel[2] = 0
            
            editedImg[row][column] = pixel

    return editedImg

# replaces all colors with the shade of gray (average of the originial r/g/b values)
def grayscale(pixels, editedImg):
	width = len(pixels)
	height = len(pixels[0])
	for row in range(width):
		for column in range(height):
			pixel = pixels[row][column]
			# calculating average of pixel color
			graycolor = (pixel[0] + pixel[1] + pixel[2]) // 3
			editedImg[row][column] = [graycolor, graycolor, graycolor]
	
	return editedImg

# changes the image into a brownish tone
def sepia(pixels, editedImg):
    width = len(pixels)
    height = len(pixels[0])

    for row in range(width):
        for column in range(height):
			# obtaining rgb pixel values
            pixel = pixels[row][column]
            r = float(pixel[0])
            g = float(pixel[1])
            b = float(pixel[2])

			# multiplying rgb values to obtain sepia filter rgb values
            sepiaR = int((r*0.393) + (g*0.769) + (b*0.189))
            sepiaG = int((r*0.349) + (g*0.686) + (b*0.168))
            sepiaB = int((r*0.272) + (g*0.534) + (b*0.131))

			# checking to see if the rgb values are over 255, if so make them equal to 255
            if sepiaR > 255:
                sepiaR = 255
            if sepiaB > 255:
                sepiaB = 255
            if sepiaG > 255:
                sepiaG = 255
            editedImg[row][column] = [sepiaR, sepiaG, sepiaB]
    return editedImg

# increase / decrease the brightness
def change_brightness(pixels, change, editedImg):
    width = len(pixels)
    height = len(pixels[0])
    for row in range(width):
        for column in range(height):
            pixel = pixels[row][column]
            if change == "decrease":
				# decreasing all the rgb values by 10
                for i in range(3):
                    if pixel[i] <= 10:
                        pixel[i] = 0
                    else:
                        pixel[i] -= 10
            elif change == "increase":
				# increasing all the rgb values by 10
                for i in range(3):
                    if pixel[i] >= 245:
                        pixel[i] = 255
                    else:
                        pixel[i] += 10
            editedImg[row][column] = pixel

    return editedImg
        
# rotate the image left/right
def rotate(pixels, direction):
    width = len(pixels)
    height = len(pixels[0])
	  # making an image with the height as the width and the width as the height 
    editedImg = display.createBlackImage(height,width) 

    if direction == "right":
        for row in range(width):
            for column in range(height):
				# row of new image = column of old image going from bottom to top, column of new image = row of old
                editedImg[height-1-column][row] = pixels[row][column]
    elif direction == "left":
        for row in range(width):
            for column in range(height):
				# row of new image = column of old, column of new image = the row of old image but going from right to left
                editedImg[column][width-1-row] = pixels[row][column]

    return editedImg

# pixelate the image
def new_pixelate(pixels):
    width = len(pixels)
    height = len(pixels[0])

    if width % 4 != 0:
        width = width - (width % 4)
    if height % 4 != 0:
        height = height - (height % 4)
    
	# creating a black image in case pixels get cut from original image
    editedImg = display.createBlackImage(width,height)
    for row in range(0,width,4):
        for column in range(0,height,4):
            average = [0,0,0]
        
            # calculating average of 4 by 4 blocks of pixels
            for i in range(4):
                for j in range(4):
                    average[0] += pixels[row+i][column+j][0]
                    average[1] += pixels[row+i][column+j][1]
                    average[2] += pixels[row+i][column+j][2]

            for i in range(3):
                average[i] = average[i] // 16
            
            # setting rgb value of every pixel in the 4 by 4 block to the average
            for i in range(4):
                for j in range(4):
                    editedImg[row+i][column+j] = average
					
    return editedImg

# create a black and white image based on a threshold value
def binarize(pixels, editedImg):
    width = len(pixels)
    height = len(pixels[0])
	# creating grayscale image of current image
    grayscaleimg = grayscale(pixels, editedImg)
    repeat = True
    initial_threshold = 0

	# getting initial threshold
    for row in range(width):
        for column in range(height):
            initial_threshold += grayscaleimg[row][column][0]
    initial_threshold = initial_threshold / (width * height)

    while repeat:
        background = []
        background_ave = 0
        foreground = []
        foreground_ave = 0
		# seperating pixels that are <= initial threshold or > initial threshold
        for row in range(width):
            for column in range(height):
                if grayscaleimg[row][column][0] <= initial_threshold:
                    background.append(grayscaleimg[row][column])
                elif grayscaleimg[row][column][0] > initial_threshold:
                    foreground.append(grayscaleimg[row][column])

		# calculating average for the seperated pixels
        for i in background:
            background_ave += i[0]
        for j in foreground:
            foreground_ave += j[0]
        background_ave = background_ave / (width * height)
        foreground_ave = foreground_ave / (width * height)

		# calculating new threshold
        newthreshold = int((background_ave + foreground_ave) // 2)
        if initial_threshold - newthreshold <= 10:
            repeat = False
        else:
            initial_threshold = newthreshold

	# changing pixels to either black or white depending if they are <= or > new threshold
    for row in range(width):
        for column in range(height):
            if grayscaleimg[row][column][0] <= newthreshold:
                grayscaleimg[row][column] = [0,0,0]
            elif grayscaleimg[row][column][0] > newthreshold:
                grayscaleimg[row][column] = [255,255,255]

    return grayscaleimg

# pixelate the image
def pixelate(pixels, editedImg):
    width = len(pixels)
    height = len(pixels[0])

    for row in range(0,width,4):
        for column in range(0,height,4):
            average = [0,0,0]
            counter = 0

			# assuming that there are 4 blocks infront and below current point
            rowend = 4 
            columnend = 4 
			# checking to see if assumption was corrent, if not then change to how many blocks are actually above/below current position
            if row + 4 >= width:
                rowend = width-row
            if column + 4 >= height:
                columnend = height-column
        
		    # calculating average of rgb pixels in 4 by 4 square
            for i in range(rowend):
                for j in range(columnend):
                    average[0] += pixels[row+i][column+j][0]
                    average[1] += pixels[row+i][column+j][1]
                    average[2] += pixels[row+i][column+j][2]
                    counter += 1

            for i in range(3):
                average[i] = average[i] // counter
        
		    # changing all the pixels in the 4 by 4 square into the average 
            for i in range(rowend):
                for j in range(columnend):
                    editedImg[row+i][column+j] = average

    return editedImg
