from selenium import webdriver
from selenium.webdriver import ActionChains
from collections import Counter
import random

# status = box class status
# key = box ID number
# element = web-click element

# opens minesweeper website
PATH = "/Users/casimerotanseco/chromedriver/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://minesweeperonline.com/#beginner")

# creates dictionary of box statuses, ID, and web-click elements for a 9x9 minesweeper grid
dict_of_box_keys_elements = {}
for i in range(1, 10):
    for j in range(1, 10):
        key_dict_variable = "x_" + str(i) + "_" + str(j)
        key_ID = str(i) + "_" + str(j)
        element = driver.find_element_by_id(key_ID)
        dict_of_box_keys_elements[key_dict_variable] = ["square blank", element]

# sets smiley face value
# facesmile = game not started or game in progress
# faceooh = mouseclick in progress
# facewin = game has been won
# facedead = gaeme over; hit bomb
face = driver.find_element_by_id("face")
val_face = face.get_attribute("class")

# game play counter and # of times to run program
counter = 0
games_to_play = 1000000

# mineseweper solver algorithm
for i in range(1, games_to_play + 1):

    print("Start Game:", i)
    counter += 1

    # click 4 corners for first move
    dict_of_box_keys_elements["x_1_1"][1].click()
    dict_of_box_keys_elements["x_1_9"][1].click()
    dict_of_box_keys_elements["x_9_1"][1].click()
    dict_of_box_keys_elements["x_9_9"][1].click()


