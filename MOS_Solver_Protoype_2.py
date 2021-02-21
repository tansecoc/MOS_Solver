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
games_to_play = 10

# mineseweper solver algorithm
for games in range(1, games_to_play + 1):

    print("Start Game:", games)
    counter += 1

    # *** START NEW GAME ***
    # creates dictionary of box statuses, ID, and web-click elements for a 9x9 minesweeper grid
    dict_of_boxes = {}
    for row in range(1, 10):
        for column in range(1, 10):
            box_ID_variable = "x_" + str(row) + "_" + str(column)
            box_ID_key = str(row) + "_" + str(column)
            box_element = driver.find_element_by_id(box_ID_key)
            dict_of_boxes[box_ID_variable] = ["square blank", box_element]

    # create safe dictionary for guessing
    safe_dict_of_boxes = {}
    for row in range(1, 10):
        for column in range(1, 10):
            safe_box_ID_variable = "x_" + str(row) + "_" + str(column)
            safe_dict_of_boxes[safe_box_ID_variable] = 0

    # set initial face value
    # facesmile = game not started or game in progress
    # faceooh = mouseclick in progress
    # facewin = game has been won
    # facedead = game over; hit bomb
    face_element = driver.find_element_by_id("face")
    face_status_value = face_element.get_attribute("class")

    # First Four Moves: click 4 corners, obtain box statuses, delete boxes from safe dictionary
    # try:
    current_box_key = "x_1_1" # sets current box key to top-left corner
    dict_of_boxes[current_box_key][1].click()  # clicks corner
    current_box_element = dict_of_boxes[current_box_key][1] # sets current box element to corner
    current_box_status = current_box_element.get_attribute("class") # obtains box status
    dict_of_boxes[current_box_key][0] = current_box_status # updates box status in box dictionary
    del safe_dict_of_boxes[current_box_key ]# deletes safe box key from safe dictionary

    current_box_key = "x_1_9" # sets current box key to top-right corner
    dict_of_boxes[current_box_key][1].click()  # clicks corner
    current_box_element = dict_of_boxes[current_box_key][1] # sets current box element to corner
    current_box_status = current_box_element.get_attribute("class") # obtains box status
    dict_of_boxes[current_box_key][0] = current_box_status # updates box status in box dictionary
    del safe_dict_of_boxes[current_box_key ]# deletes safe box key from safe dictionary

    current_box_key = "x_9_1" # sets current box key to bottom-left corner
    dict_of_boxes[current_box_key][1].click()  # clicks corner
    current_box_element = dict_of_boxes[current_box_key][1] # sets current box element to corner
    current_box_status = current_box_element.get_attribute("class") # obtains box status
    dict_of_boxes[current_box_key][0] = current_box_status # updates box status in box dictionary
    del safe_dict_of_boxes[current_box_key ]# deletes safe box key from safe dictionary

    current_box_key = "x_9_9" # sets current box key to bottom-right corner
    dict_of_boxes[current_box_key][1].click()  # clicks corner
    current_box_element = dict_of_boxes[current_box_key][1] # sets current box element to corner
    current_box_status = current_box_element.get_attribute("class") # obtains box status
    dict_of_boxes[current_box_key][0] = current_box_status # updates box status in box dictionary
    del safe_dict_of_boxes[current_box_key ]# deletes safe box key from safe dictionary
    # except:
    #     continue

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
            current_box_key = random.choice(list(safe_dict_of_boxes.keys())) # sets random current box
            current_box_element = dict_of_boxes[current_box_key][1] # sets current box web-click element
            current_box_element.click() # clicks current box

            # obtain current box status, deletes current box from safe dictionary
            current_box_status = current_box_element.get_attribute("class") # obtains box status
            dict_of_boxes[current_box_key][0] = current_box_status  # updates box status in box dictionary
            del safe_dict_of_boxes[current_box_key]  # deletes safe box key from safe dictionary
            print("Clicked box:", current_box_key + ". Status:", current_box_status)

            # check status of boxes that surround current box and implement All-Free-Neighbors (AFN) logic

            # parse current box into a list to obtain starting point for surrounding boxes
            current_box_parse = list(current_box_key)

            # *** BEGIN OBTAINING SURROUNDING BOX STATUSES ***

            # TOP-LEFT obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_TL_box_key = "No box"
            surround_TL_box_status = "null"
            surround_TL_box_element = ""
            try:
                # get box coorindates
                surround_TL_box_key = "x_" + str(int(current_box_parse[2]) - 1) + "_" \
                                      + str(int(current_box_parse[4]) - 1)
                # get box status
                surround_TL_box_element = dict_of_boxes[surround_TL_box_key][1] # get box web element
                surround_TL_box_status = surround_TL_box_element.get_attribute("class") # obtain box status
                dict_of_boxes[surround_TL_box_key][0] = surround_TL_box_status  # updates box status in box dictionary

                if surround_TL_box_status == "square open0":
                    del safe_dict_of_boxes[surround_TL_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # TOP-MIDDLE obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_TM_box_key = "No box"
            surround_TM_box_status = "null"
            surround_TM_box_element = ""
            try:
                # get box coorindates
                surround_TM_box_key = "x_" + str(int(current_box_parse[2]) - 1) + "_" \
                                      + str(int(current_box_parse[4]))
                # get box status
                surround_TM_box_element = dict_of_boxes[surround_TM_box_key][1]  # get box web element
                surround_TM_box_status = surround_TM_box_element.get_attribute("class")  # obtain box status
                dict_of_boxes[surround_TM_box_key][0] = surround_TM_box_status  # updates box status in box dictionary

                if surround_TM_box_status == "square open0":
                    del safe_dict_of_boxes[surround_TM_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # TOP-RIGHT obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_TR_box_key = "No box"
            surround_TR_box_status = "null"
            surround_TR_box_element = ""
            try:
                # get box coorindates
                surround_TR_box_key = "x_" + str(int(current_box_parse[2]) - 1) + "_" \
                                      + str(int(current_box_parse[4]) + 1)
                # get box status
                surround_TR_box_element = dict_of_boxes[surround_TR_box_key][1]  # get box web element
                surround_TR_box_status = surround_TR_box_element.get_attribute("class")  # obtain box status
                dict_of_boxes[surround_TR_box_key][0] = surround_TR_box_status  # updates box status in box dictionary

                if surround_TR_box_status == "square open0":
                    del safe_dict_of_boxes[surround_TR_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # LEFT-MIDDLE BOX obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_LM_box_key = "No box"
            surround_LM_box_status = "null"
            surround_LM_box_element = ""
            try:
                # get box coorindates
                surround_LM_box_key = "x_" + str(int(current_box_parse[2])) + "_" \
                                      + str(int(current_box_parse[4]) - 1)
                # get box status
                surround_LM_box_element = dict_of_boxes[surround_LM_box_key][1]  # get box web element
                surround_LM_box_status = surround_LM_box_element.get_attribute("class")  # obtain box status
                dict_of_boxes[surround_LM_box_key][0] = surround_LM_box_status  # updates box status in box dictionary

                if surround_LM_box_status == "square open0":
                    del safe_dict_of_boxes[surround_LM_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # RIGHT-MIDDLE BOX obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_RM_box_key = "No box"
            surround_RM_box_status = "null"
            surround_RM_box_element = ""
            try:
                # get box coorindates
                surround_RM_box_key = "x_" + str(int(current_box_parse[2])) + "_" \
                                      + str(int(current_box_parse[4]) + 1)
                # get box status
                surround_RM_box_element = dict_of_boxes[surround_RM_box_key][1]  # get box web element
                surround_RM_box_status = surround_RM_box_element.get_attribute("class")  # obtain box status
                dict_of_boxes[surround_RM_box_key][0] = surround_RM_box_status  # updates box status in box dictionary

                if surround_RM_box_status == "square open0":
                    del safe_dict_of_boxes[surround_RM_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # BOTTOM-LEFT BOX obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_BL_box_key = "No box"
            surround_BL_box_status = "null"
            surround_BL_box_element = ""
            try:
                # get box coorindates
                surround_BL_box_key = "x_" + str(int(current_box_parse[2]) + 1) + "_" \
                                      + str(int(current_box_parse[4]) - 1)
                # get box status
                surround_BL_box_element = dict_of_boxes[surround_BL_box_key][1]  # get box web element
                surround_BL_box_status = surround_BL_box_element.get_attribute("class")  # obtain box status
                dict_of_boxes[surround_BL_box_key][0] = surround_BL_box_status  # updates box status in box dictionary

                if surround_BL_box_status == "square open0":
                    del safe_dict_of_boxes[surround_BL_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # BOTTOM-MIDDLE BOX obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_BM_box_key = "No box"
            surround_BM_box_status = "null"
            surround_BM_box_element = ""
            try:
                # get box coorindates
                surround_BM_box_key = "x_" + str(int(current_box_parse[2]) + 1) + "_" \
                                      + str(int(current_box_parse[4]))
                # get box status
                surround_BM_box_element = dict_of_boxes[surround_BM_box_key][1]  # get box web element
                surround_BM_box_status = surround_BM_box_element.get_attribute("class")  # obtain box status
                dict_of_boxes[surround_BM_box_key][0] = surround_BM_box_status  # updates box status in box dictionary

                if surround_BM_box_status == "square open0":
                    del safe_dict_of_boxes[surround_BM_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # BOTTOM-RIGHT BOX obtain box key and status, deletes from safe dictionary if "square open" == 0
            surround_BR_box_key = "No box"
            surround_BR_box_status = "null"
            surround_BR_box_element = ""
            try:
                # get box coorindates
                surround_BR_box_key = "x_" + str(int(current_box_parse[2]) + 1) + "_" \
                                      + str(int(current_box_parse[4]) + 1)
                # get box status
                surround_BR_box_element = dict_of_boxes[surround_BR_box_key][1]  # get box web element
                surround_BR_box_status = surround_BR_box_element.get_attribute("class")  # obtain box status
                dict_of_boxes[surround_BR_box_key][0] = surround_BR_box_status  # updates box status in box dictionary

                if surround_BR_box_status == "square open0":
                    del safe_dict_of_boxes[surround_BR_box_key]  # deletes safe box key from safe dictionary
            except:
                pass

            # ***THIS CODE IS FOR TESTING THE SURROUNDING BOXES***

            # Surrounding box keys and statuses
            print("TL box key:", surround_TL_box_key + ". Status:", surround_TL_box_status)
            print("TM box key:", surround_TM_box_key + ". Status:", surround_TM_box_status)
            print("TR box key:", surround_TR_box_key + ". Status:", surround_TR_box_status)
            print("LM box key:", surround_LM_box_key + ". Status:", surround_LM_box_status)
            print("RM box key:", surround_RM_box_key + ". Status:", surround_RM_box_status)
            print("BL box key:", surround_BL_box_key + ". Status:", surround_BL_box_status)
            print("BM box key:", surround_BM_box_key + ". Status:", surround_BM_box_status)
            print("BR box key:", surround_BR_box_key + ". Status:", surround_BR_box_status)

            # Surrounding box elements
            # print("TL box element:", surround_TL_box_element)
            # print("TM box element:", surround_TM_box_element)
            # print("TR box element:", surround_TR_box_element)
            # print("LM box element:", surround_LM_box_element)
            # print("RM box element:", surround_RM_box_element)
            # print("BL box element:", surround_BL_box_element)
            # print("BM box element:", surround_BM_box_element)
            # print("BR box element:", surround_BR_box_element)

            # *** Placeholder - delete surrounding boxes whose status == square open0 from safe dictionary

            # obtain number of bombs surrounding current box
            free_neighbors_count = 0
            try:
                free_neighbors_count = int(current_box_status[-1])
            except:
                pass

            # skip AFN logic if current box value is blank
            if free_neighbors_count == 0:
                pass

            # apply AFN logic
            else:

                # create surrounding box status dictionary
                surrounding_box_status_dict = {
                    surround_TL_box_key:surround_TL_box_status,
                    surround_TM_box_key:surround_TM_box_status,
                    surround_TR_box_key:surround_TR_box_status,
                    surround_LM_box_key:surround_LM_box_status,
                    surround_RM_box_key:surround_RM_box_status,
                    surround_BL_box_key:surround_BL_box_status,
                    surround_BM_box_key:surround_BM_box_status,
                    surround_BR_box_key:surround_BR_box_status
                    }

                # creates surrounding box status counter
                surrounding_box_status_counter = Counter(surrounding_box_status_dict.values())

                print("Surrounding box status dictionary:", surrounding_box_status_dict)
                print("Surrounding box status counter:", surrounding_box_status_counter)

                # checks if current box value matches number of blank surrounding boxes
                # if so, then flag all blank surrounding boxes
                if free_neighbors_count == surrounding_box_status_counter["square blank"]:

                    # print("MATCH: Free neighbor count:", free_neighbors_count, ". Square Blank:",
                    #       surrounding_box_status_counter["square blank"])

                    # surround TL box flag check
                    if surround_TL_box_status == "square blank":
                        actionChains.context_click(surround_TL_box_element).perform()
                        surround_TL_box_status = "square bombflagged"
                        dict_of_boxes[surround_TL_box_key][0] = \
                            surround_TL_box_status  # updates box status in box dictionary
                        print("Flagged:", surround_TL_box_key)



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