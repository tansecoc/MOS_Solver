from selenium import webdriver
from selenium.webdriver import ActionChains
from collections import Counter
import random
import copy

# box_status = box class status
# box_ID = box ID number
# box_element = web-click element

# opens minesweeper website
PATH = "/Users/casimerotanseco/chromedriver/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://minesweeperonline.com/#beginner")

# creates dictionary of box statuses, ID, and web-click elements for a 9x9 minesweeper grid
dict_of_boxes = {}
for i in range(1, 10):
    for j in range(1, 10):
        box_ID_variable = "x_" + str(i) + "_" + str(j)
        box_ID_key = str(i) + "_" + str(j)
        box_element = driver.find_element_by_id(box_ID_key)
        dict_of_boxes[box_ID_variable] = ["square blank", box_element]

# create safe dictionary for guessing
safe_dict_of_boxes = {}
for i in range(1, 10):
    for j in range(1, 10):
        safe_box_ID_variable = "x_" + str(i) + "_" + str(j)
        safe_dict_of_boxes[safe_box_ID_variable] = 0

# set initial face value
# facesmile = game not started or game in progress
# faceooh = mouseclick in progress
# facewin = game has been won
# facedead = game over; hit bomb
face_element = driver.find_element_by_id("face")
face_status_value = face_element.get_attribute("class")

# game play counter and # of times to run program
counter = 0
games_to_play = 10

# mineseweper solver algorithm
for i in range(1, games_to_play + 1):

    print("Start Game:", i)
    counter += 1

    # click 4 corners as first four moves then delete boxes from safe dictionary
    four_box_counter = 1
    if four_box_counter < 1:
        dict_of_boxes["x_1_1"][1].click()
        del safe_dict_of_boxes["x_1_1"]
        dict_of_boxes["x_1_9"][1].click()
        del safe_dict_of_boxes["x_1_9"]
        dict_of_boxes["x_9_1"][1].click()
        del safe_dict_of_boxes["x_9_1"]
        dict_of_boxes["x_9_9"][1].click()
        del safe_dict_of_boxes["x_9_9"]
        four_box_counter += 1

    # check face value
    face_element = driver.find_element_by_id("face")
    face_status_value = face_element.get_attribute("class")

    # pause program if won
    if face_status_value == "facewin":
        input("YOU HAVE WON! PROGRAM PAUSED!!!")

    # restart game if face == dead
    if face_status_value == "facedead":
        face_element.click()

    # begin click guesses
    else:
        # if face is != 'facedead' then continue guesses
        while face_status_value != "facedead" or face_status_value != "facewin":

            # click random box
            current_box_key = random.choice(list(dict_of_boxes.keys()))
            current_box_element = dict_of_boxes[current_box_key][1]
            current_box_status = current_box_element.get_attribute("class")

            # if current_box_status ==

            print("Current box status:", current_box_status)
            current_box_element.click()

            current_box_status = current_box_element.get_attribute("class")
            print("Current box status:", current_box_status)

            # check face value after click
            face_element = driver.find_element_by_id("face")
            face_status_value = face_element.get_attribute("class")
            print("Face value status:", face_status_value)

            # pause program if won
            if face_status_value == "facewin":
                input("YOU HAVE WON! PROGRAM PAUSED!!!")
