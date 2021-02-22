from selenium import webdriver
from selenium.webdriver import ActionChains
from collections import Counter
import random
import time

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
games_to_play = 1000

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
        print("Clicked box:", str(current_box_key) + ". Status:", dict_of_boxes[current_box_key][0])
        print("Deleted box:", current_box_key)
        del safe_dict_of_boxes[current_box_key]  # deletes safe box key from safe dictionary

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
            print("Clicked box:", str(current_box_key) + ". Status:", dict_of_boxes[current_box_key][0])
            print("Deleted box:", current_box_key)
            del safe_dict_of_boxes[current_box_key]  # deletes box key from safe dictionary

            print(len(safe_dict_of_boxes))
            if len(safe_dict_of_boxes) == 9 and dict_of_boxes[current_box_key][0] != "square bombrevealed":
                input("PROGRAM PAUSED!!! YOU WON!!!!")

            # check status of boxes that surround current box and implement All-Free-Neighbors (AFN) logic

            # parse current box into a list to obtain starting coordinates for surrounding boxes
            current_box_coordinates = (current_box_key)
            # print("Current box coordinates:", current_box_coordinates)

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
                    # update surrounding box statuses
                    dict_of_boxes[number][0] = dict_of_boxes[number][1].get_attribute("class")
                    print("The updated status of box", number, "is:", dict_of_boxes[number][0])
                    surrounding_box_dict[number] = dict_of_boxes[number][0]  # adds box status as value
                except:
                    continue

            print("Surrounding box dictionary:", surrounding_box_dict)

            # delete 'square open0' boxes from safe box dictionary
            for key in surrounding_box_dict:
                if dict_of_boxes[key][0] == "square open0":
                    try:
                        print("Deleted box:", key)
                        del safe_dict_of_boxes[key]  # deletes box key from safe dictionary
                    except:
                        pass

            print("Safe box dict:", safe_dict_of_boxes)

            current_box_mine_neighbors = []
            try:
                current_box_mine_neighbors = int(current_box_status[-1])
                print("Current box:", str(current_box_key) + ". Current box mine neighbors:",
                      str(current_box_mine_neighbors))
            except:
                pass

            if current_box_mine_neighbors != 0 and current_box_mine_neighbors != []:
                for key in surrounding_box_dict:
                    surrounding_box_status_counter = Counter(surrounding_box_dict.values())
                print("Surrounding box status counter:", surrounding_box_status_counter)

                if current_box_mine_neighbors == surrounding_box_status_counter["square blank"]:
                    print("Mine neighbors match blank surrounding squares.  Initiating flag sequence.")
                    for key in surrounding_box_dict:
                        print("Neighbor key:", key, ", Neighbor value:", dict_of_boxes[key][0])
                        if dict_of_boxes[key][0] == "square blank":
                            # print("A flag will be placed on key:", key, "with status of", dict_of_boxes[key][0])
                            # key_element_to_flag = dict_of_boxes[key][1]
                            # actionChains.context_click(key_element_to_flag).perform()
                            # dict_of_boxes[key][0] = "square bombflagged"
                            # surrounding_box_dict[key] = dict_of_boxes[key][0]

                            try:
                                print("Key:", key, "with status of", dict_of_boxes[key][0], "will be avoided")
                                dict_of_boxes[key][0] = "square bombflagged"
                                del safe_dict_of_boxes[key]  # deletes box key from safe dictionary
                            except:
                                pass

                    for key in surrounding_box_dict:
                        surrounding_box_status_counter = Counter(surrounding_box_dict.values())
                    print("Refreshed surrounding box status counter:", surrounding_box_status_counter)

                    # input("stop")



            # input("stop")

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