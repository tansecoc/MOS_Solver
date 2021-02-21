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

# enables mouse left-click
actionChains = ActionChains(driver)

# game play counter and # of times to run program
counter = 0
games_to_play = 100

# mineseweper solver algorithm
for games in range(1, games_to_play + 1):

    print("Start Game:", games)
    counter += 1

    # *** START NEW GAME ***
    # creates dictionary of box statuses, ID, and web-click elements for a 9x9 minesweeper grid
    dict_of_boxes = {}
    for row in range(1, 10):
        for column in range(1, 10):
            box_ID_coordinate = (int(row), int(column))
            box_ID_key = str(row) + "_" + str(column)
            box_element = driver.find_element_by_id(box_ID_key)
            dict_of_boxes[box_ID_coordinate] = ["square blank", box_element, box_ID_key]
    # print("Starting dict of boxes:", dict_of_boxes)

    # create safe dictionary for guessing
    safe_dict_of_boxes = {}
    for row in range(1, 10):
        for column in range(1, 10):
            safe_box_ID_coordinate = (int(row), int(column))
            safe_dict_of_boxes[safe_box_ID_coordinate] = 0
    # print("starting safe dict:", safe_dict_of_boxes)


    # set initial face value
    # facesmile = game not started or game in progress
    # faceooh = mouseclick in progress
    # facewin = game has been won
    # facedead = game over; hit bomb
    face_element = driver.find_element_by_id("face")
    face_status_value = face_element.get_attribute("class")
    # print("starting face value:", face_status_value)

    # First Four Moves: click 4 corners, obtain box statuses, delete boxes from safe dictionary
    # try:
    corner_box_list = [(1,1), (1,9), (9,1), (9,9)]
    for corner_key in corner_box_list:
        current_box_key = corner_key  # sets current box key to top-left corner
        dict_of_boxes[current_box_key][1].click()  # clicks corner
        current_box_element = dict_of_boxes[current_box_key][1]  # sets current box element to corner
        current_box_status = current_box_element.get_attribute("class")  # obtains box status
        dict_of_boxes[current_box_key][0] = current_box_status  # updates box status in box dictionary
        del safe_dict_of_boxes[current_box_key]  # deletes safe box key from safe dictionary
        print("Clicked box:", str(current_box_key) + ". Status:", dict_of_boxes[current_box_key][0])

    # check face value
    face_element = driver.find_element_by_id("face")
    face_status_value = face_element.get_attribute("class")

    # pause program if won
    if face_status_value == "facewin":
        input("YOU HAVE WON! PROGRAM PAUSED!!!")

    # restart game if face == dead
    elif face_status_value == "facedead":
        face_element.click()
        print("Face value status:", face_status_value + ". Restarting game.")
        continue

    # begin click guesses
    else:

        # if game is not dead or won then continue guessing loop
        while face_status_value != "facedead" or face_status_value != "facewin":

            # click random box from safe dictionary
            current_box_key = random.choice(list(safe_dict_of_boxes.keys()))  # sets random current box
            current_box_element = dict_of_boxes[current_box_key][1]  # sets current box web-click element
            current_box_element.click()  # clicks current box

            # obtain current box status, deletes current box from safe dictionary
            current_box_status = current_box_element.get_attribute("class")  # obtains box status
            dict_of_boxes[current_box_key][0] = current_box_status  # updates box status in box dictionary
            del safe_dict_of_boxes[current_box_key]  # deletes box key from safe dictionary
            print("Clicked box:", str(current_box_key) + ". Status:", dict_of_boxes[current_box_key][0])

            # check status of boxes that surround current box and implement All-Free-Neighbors (AFN) logic

            # parse current box into a list to obtain starting coordinates for surrounding boxes
            current_box_coordinates = (current_box_key)
            print("Current box coordinates:", current_box_coordinates)

            coordinate_offsets = [(-1, -1), (-1, 0), (-1, 1),
                                  (0, -1), (0, 1),
                                  (1, -1), (1, 0), (1, 1)]

            surrounding_box_coordinates = []
            for number in range(len(coordinate_offsets)):
                surrounding_box_coordinates.append(tuple(map(lambda x, y: x + y,
                                                             coordinate_offsets[number], current_box_coordinates)))

            print("Surrounding box coordinates:", surrounding_box_coordinates)

            # create surrounding box dictionary
            surrounding_box_dict = {}
            for number in surrounding_box_coordinates:
                try:
                    surrounding_box_dict[number] = [dict_of_boxes[number][0], dict_of_boxes[number][1]]
                except:
                    continue

            print(surrounding_box_dict)
            input("stop")

            # *** BEGIN OBTAINING SURROUNDING BOX STATUSES ***



            # ***THIS CODE IS FOR TESTING***
            # print("Dict of boxes:")
            # for keys in dict_of_boxes:
            #     print(keys, dict_of_boxes[keys][0])
            # print("Safe dict of boxes:", safe_dict_of_boxes)
            # input("stop")


            # *** END OBTAINING SURROUNDING BOX STATUSES ***

            # END OF WHILE LOOP - check face value after click
            face_element = driver.find_element_by_id("face")
            face_status_value = face_element.get_attribute("class")

            # pause program if won
            if face_status_value == "facewin":
                print("Face value status:", face_status_value)
                input("YOU HAVE WON! PROGRAM PAUSED!!!")

            # restart guessing while loop
            if face_status_value == "facedead":
                print("Face value status:", face_status_value + ". Restarting game.")
                face_element.click()
                break