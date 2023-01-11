# Description: Given an image, this program manipulates images using basic, intermediate and advanced functions of the user's choice. These manipulations stack on top of each other. The user can also quit the progam, open an image from their computer, save their current image, and reload the original image.

import display
import manipulation
import tkinter.filedialog
import pygame
pygame.init()

# list of system options
system = [
            "Q: Quit",
            "O: Open Image",
            "S: Save Current Image",
            "R: Reload Original Image",
         ]

# list of basic operation options
basic = [
          "1: Invert",
          "2. Flip Horizontal",
          "3. Flip Vertical",
          "4: Switch to Intermeidate Functions",
          "5: Switch to Advanced Functions"
        ]

# list of intermediate operation options
intermediate = [
                    "1: Remove Red Channel",
                    "2: Remove Green Channel",
			        "3: Remove Blue Channel",
                    "4: Convert to Grayscale", 
		            "5: Apply Sepia Filter", 
                    "6: Decrease Brightness", 
			        "7: Increase Brightness", 
                    "8: Switch to Basic Functions",
			        "9: Switch to Advanced Functions"
                ]

# list of advanced operation options
advanced = [
                "1: Rotate Left",
				"2: Rotate Right", 
				"3: Pixelate",
				"4: Binarize",
				"5: Switch to Basic Functions",
                "6: Switch to Intermediate Functions"
            ]

# a helper function that generates a list of strings to be displayed in the interface
def generateMenu(state):
    """
    Input:  state - a dictionary containing the state values of the application
    Returns: a list of strings, each element represets a line in the interface
    """
    menuString = ["Welcome to Image Processer!"]
    menuString.append("") # an empty line
    menuString.append("Choose the following options:")
    menuString.append("") # an empty line
    menuString += system
    menuString.append("") # an empty line

    # build the list differently depending on the mode attribute
    if state["mode"] == "basic":
        menuString.append("--Basic Mode--")
        menuString += basic
        menuString.append("")
        menuString.append("Enter your choice (Q/O/S/R or 1-5)")
    elif state["mode"] == "intermediate":
        menuString.append("--Intermediate Mode--")
        menuString += intermediate
        menuString.append("")
        menuString.append("Enter your choice (Q/O/S/R or 1-9)")
    elif state["mode"] == "advanced":
        menuString.append("--Advanced Mode--")
        menuString += advanced
        menuString.append("")
        menuString.append("Enter your choice (Q/O/S/R or 1-6)")
    else:
        menuString.append("Error: Unknown mode!")

    return menuString

# a helper function that returns the result image as a result of the operation chosen by the user
# it also updates the state values when necessary (e.g, the mode attribute if the user switches mode)
def handleUserInput(state, img):
    """
        Input:  state - a dictionary containing the state values of the application
                img - the 2d array of RGB values to be operated on
        Returns: the 2d array of RGB vales of the result image of an operation chosen by the user
    """
    userInput = state["lastUserInput"].upper()
    # handle the system functionalities
    if userInput.isalpha(): # check if the input is an alphabet
        print("Log: Doing system functionalities " + userInput)
        if userInput == "Q": # this case actually won't happen, it's here as an example
            print("Log: Quitting...")
        elif userInput == "O": # open image
            tkinter.Tk().withdraw()
            state["lastOpenFilename"] = tkinter.filedialog.askopenfilename()
            img = display.getImage(state["lastOpenFilename"])
        elif userInput == "S": # save image
            tkinter.Tk().withdraw()
            state["lastSaveFilename"] = tkinter.filedialog.asksaveasfilename()
            display.saveImage(img, state["lastSaveFilename"])
        elif userInput == "R": # reload original image
            img = display.getImage(state["lastOpenFilename"])

        # ***add the rest to handle other system functionalities***
    # or handle the manipulation functionalities based on which mode the application is in
    elif userInput.isdigit(): # has to be a digit for manipulation options
        print("Log: Doing manipulation functionalities " + userInput)
        editedImg = display.createBlackImage(len(img),len(img[0])) # create the image that will be edited depending on the command inputed
        if state["mode"] == "basic":
            if userInput == "1":
                img = manipulation.invert(img, editedImg) # invert image
            elif userInput == "2":
                img = manipulation.flipHorizontal(img, editedImg) # flip image horizontally
            elif userInput == "3":
                img = manipulation.flipVertical(img, editedImg) # flip image vertically
            elif userInput == "4":
                state["mode"] = "intermediate" # change state to intermediate
            elif userInput == "5":
                state["mode"] = "advanced" # change state to advanced
                   
        elif state["mode"] == "intermediate":
            if userInput == "1":
                img = manipulation.remove_color(img, "red", editedImg) # remove red from image
            elif userInput == "2":
                img = manipulation.remove_color(img, "green", editedImg) # remove green from image
            elif userInput == "3":
                img = manipulation.remove_color(img, "blue", editedImg) # remove blue from image
            elif userInput == "4":
                img = manipulation.grayscale(img, editedImg) # change image to grayscale
            elif userInput == "5":
                img = manipulation.sepia(img, editedImg) # apply sepia filter to rgb values
            elif userInput == "6":
                img = manipulation.change_brightness(img, "decrease", editedImg) # decrease brightness of image
            elif userInput == "7":
                img = manipulation.change_brightness(img, "increase", editedImg) # increase brightness of image
            elif userInput == "8":
                state["mode"] = "basic" # change mode to basic
            elif userInput == "9":
                state["mode"] = "advanced" # chnage mode to advanced

        elif state["mode"] == "advanced":
            if userInput == "1":
                img = manipulation.rotate(img, "left") # rotate image left by 90 degrees
            elif userInput == "2":
                img = manipulation.rotate(img, "right") # rotate image right by 90 degrees
            elif userInput == "3":
                img = manipulation.new_pixelate(img) # pixelate image
            elif userInput == "4":
                img = manipulation.binarize(img, editedImg) # binarize image
            elif userInput == "5":
                state["mode"] = "basic" # change mode to basic
            elif userInput == "6":
                state["mode"] = "intermediate" # change mode to intermediate
    else: # unrecognized user input
        print("Log: Unrecognized user input: " + userInput)

    display.showInterface(img, "Current Image", generateMenu(state))
    return img

# use a dictionary to remember several state values of the application
appStateValues = {
                    "mode": "basic",
                    "lastOpenFilename": "",
                    "lastSaveFilename": "",
                    "lastUserInput": ""
                 }

currentImg = display.createBlackImage(600, 400) # create a default 600 x 400 black image
display.showInterface(currentImg, "No Image", generateMenu(appStateValues)) # note how it is used

# ***this is the event-loop of the application. Keep the remainder of the code unmodified***
keepRunning = True
# a while-loop getting events from pygame
while keepRunning:
    ### use the pygame event handling system ###
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            appStateValues["lastUserInput"] = pygame.key.name(event.key)
            # prepare to quit the loop if user inputs "q" or "Q"
            if appStateValues["lastUserInput"].upper() == "Q":
                keepRunning = False
            # otherwise let the helper function handle the input
            else:
                currentImg = handleUserInput(appStateValues, currentImg)
        elif event.type == pygame.QUIT: #another way to quit the program is to click the close botton
            keepRunning = False

# shutdown everything from the pygame package
pygame.quit()

print("Log: Program Quit")