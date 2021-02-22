from selenium import webdriver
from selenium.webdriver import ActionChains
from collections import Counter
import random

# opens minesweeper website
PATH = "/Users/casimerotanseco/chromedriver/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://minesweeperonline.com/#beginner")

# game play counter and # of times to run program
counter = 0
games_to_play = 1000

# mineseweper solver algorithm
for games in range(1, games_to_play + 1):

    # *** START NEW GAME ***
    print("Start Game:", games)
    counter += 1

    # creates dictionary of box statuses, ID, and web-click elements for a 9x9 minesweeper grid
    dict_of_boxes = {}
    for row in range(1, 10):
        for column in range(1, 10):
            box_ID_coordinate = (int(row), int(column))
            box_ID_key = str(row) + "_" + str(column)
            box_element = driver.find_element_by_id(box_ID_key)
            dict_of_boxes[box_ID_coordinate] = ["square blank", box_element, box_ID_key]
    # [0] = box status
    # [1] = box element
    # [2] = box ID label

    # create safe dictionary for guessing
    safe_dict_of_boxes = {}
    for row in range(1, 10):
        for column in range(1, 10):
            safe_dict_of_boxes[(int(row), int(column))] = 0

    print("Values remaining in safe dict:", len(safe_dict_of_boxes))

    # Coordinate offsets for AMN logic
    coordinate_offsets = [(-1, -1), (-1, 0), (-1, 1),
                          (0, -1), (0, 1),
                          (1, -1), (1, 0), (1, 1)]

    # First Four Moves: click 4 corners, obtain box statuses, delete boxes from safe dictionary
    corner_box_list = [(1, 1), (1, 9), (9, 1), (9, 9)]
    for corner_key in corner_box_list:

        # click corner
        current_box_key = corner_key  # sets current box key to corner
        dict_of_boxes[current_box_key][1].click()  # clicks corner web element
        print("Clicked box:", str(current_box_key))

        # obtain box status and updates in main dictionary
        current_box_element = dict_of_boxes[current_box_key][1]  # sets current box element to corner
        current_box_status = current_box_element.get_attribute("class")  # obtains box status
        dict_of_boxes[current_box_key][0] = current_box_status  # updates box status in box dictionary
        print("Box:", str(current_box_key), "Status:", dict_of_boxes[current_box_key][0])

        # deletes safe box key from safe dictionary
        del safe_dict_of_boxes[current_box_key]
        print("Deleted box:", current_box_key)

        print("Values remaining in safe dict:", len(safe_dict_of_boxes))

    # check face value
    face_element = driver.find_element_by_id("face")
    face_status_value = face_element.get_attribute("class")

    # restart game if face == dead
    if face_status_value == "facedead":
        face_element.click()
        print("Face value status:", face_status_value + ". GAME OVER.  Restarting game...")
        continue

    # ***BEGIN GUESSES LOOP***
    else:

        # if game is not dead or won then continue guessing loop
        while face_status_value != "facedead":

            # click random box from safe dictionary
            current_box_key = random.choice(list(safe_dict_of_boxes.keys()))  # pull random key from safe dict
            current_box_element = dict_of_boxes[current_box_key][1]  # sets current box web-click element
            current_box_element.click()  # clicks current box
            print("Clicked box:", str(current_box_key))

            # obtain box status and updates in main dictionary
            current_box_element = dict_of_boxes[current_box_key][1]  # sets current box element to corner
            current_box_status = current_box_element.get_attribute("class")  # obtains box status
            dict_of_boxes[current_box_key][0] = current_box_status  # updates box status in box dictionary
            print("Box:", str(current_box_key), "Status:", dict_of_boxes[current_box_key][0])

            # deletes safe box key from safe dictionary
            del safe_dict_of_boxes[current_box_key]
            print("Deleted box:", current_box_key)

            # prints count of values remaining in safe dict and prints entire safe dict
            print("Values remaining in safe dict:", len(safe_dict_of_boxes))
            # print("Safe dict of boxes:", safe_dict_of_boxes)

            # test to catch win
            if len(safe_dict_of_boxes) == 10 and dict_of_boxes[current_box_key][0] != "square bombrevealed":
                input("PROGRAM PAUSED!!! YOU WON!!!!")

            # ***START AMN LOGIC***

            # create list of coordinates for coordinates that surround the current box
            surrounding_box_coordinates = []
            for number in range(len(coordinate_offsets)):
                surrounding_box_coordinates.append(tuple(map(lambda x, y: x + y,
                                                             coordinate_offsets[number], current_box_key)))
            # print("Surrounding box coordinates:", surrounding_box_coordinates)

            # create surrounding box dictionary to obtain statuses
            surrounding_box_dict = {}
            for coordinate in surrounding_box_coordinates:
                try:
                    # update surrounding box statuses in main dictionary
                    dict_of_boxes[coordinate][0] = dict_of_boxes[coordinate][1].get_attribute("class")
                    surrounding_box_dict[coordinate] = dict_of_boxes[coordinate][0]  # adds box status as value
                except:
                    continue
            # print("Dict of boxes:", dict_of_boxes)
            # print("Surrounding box dict:", surrounding_box_dict)

            # delete 'square open0' boxes from safe box dictionary
            for key in surrounding_box_dict:
                if dict_of_boxes[key][0] == "square open0":
                    try:
                        del safe_dict_of_boxes[key]  # deletes box key from safe dictionary
                        print("Deleted surrounding box:", key, "Status:", dict_of_boxes[key][0])
                    except:
                        pass

            print("Dict of boxes:", dict_of_boxes)
            print("Surrounding box dict:", surrounding_box_dict)





            # END OF WHILE LOOP - check face value after click
            face_element = driver.find_element_by_id("face")
            face_status_value = face_element.get_attribute("class")

            # restart guessing while loop
            if face_status_value == "facedead":
                input("stop")
                print("Face value status:", face_status_value + ". Restarting game.")
                face_element.click()
                break

# 2. Test list size comparison
# 3. Use get function in dictionary to get key value, but if value does not appear then return default value
# 4. Create board box value refresh function