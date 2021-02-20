from selenium import webdriver
from selenium.webdriver import ActionChains
from collections import Counter
import random

# opens minesweeper website
PATH = "/Users/casimerotanseco/chromedriver/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://minesweeperonline.com/#beginner")

# enables mouse left-click
actionChains = ActionChains(driver)

# creates list of box variables
list_of_box_variables = []
for i in range(1, 10):
    for j in range(1, 10):
        list_of_box_variables.append("x_" + str(i) + "_" + str(j))

# creates list of box IDs
list_of_box_IDs = []
for i in range(1, 10):
    for j in range(1, 10):
        list_of_box_IDs.append(str(i) + "_" + str(j))

# creates list of box variables
dict_of_box_variables = {}
for item in range(len(list_of_box_variables)):
    key = list_of_box_variables[item]
    value = driver.find_element_by_id(list_of_box_IDs[item])
    dict_of_box_variables[key] = value

# sets face value
face = driver.find_element_by_id("face")
val_face = face.get_attribute("class")
counter = 0

games_to_play = 1000

for i in range(1, games_to_play + 1):
    # begins guess algorithm
    print("Game:", i)

    counter += 1

    # click 4 corners
    x_1_1 = dict_of_box_variables["x_1_1"]
    x_1_9 = dict_of_box_variables["x_1_9"]
    x_9_1 = dict_of_box_variables["x_9_1"]
    x_9_9 = dict_of_box_variables["x_9_9"]
    x_1_1.click()
    x_1_9.click()
    x_9_1.click()
    x_9_9.click()

    # check face value
    face = driver.find_element_by_id("face")
    val_face = face.get_attribute("class")

    if val_face == "facedead":
        # restart game if face == dead
        face.click()

    else:
        # begin click guesses

        while val_face != "facedead":

            # obtain value of face
            val_face = face.get_attribute("class")

            # click random box
            current_box_key = random.choice(list(dict_of_box_variables.keys()))
            current_box_value = dict_of_box_variables[current_box_key]
            current_box_status = current_box_value.get_attribute("class")

            if current_box_status == "square blank":

                current_box_value.click()

                # obtain value of clicked box
                current_box_status = current_box_value.get_attribute("class")
                print("Current box key:", current_box_key, ", Status:", current_box_status)

                # if all values of open boxes surrounding current box == "square blank" then mark with flags
                # obtain value of surrounding boxes

                # parse current box into list
                current_box_parse = list(current_box_key)

                # build surrounding box status dictionary
                surrounding_box_status_dict = {}

                # obtain top-left box key and status
                top_left_box_status = ""
                try:
                    top_left_box_key = "x_" + str(int(current_box_parse[2])-1) + "_" + str(int(current_box_parse[4])-1)
                    top_left_box_value = dict_of_box_variables[top_left_box_key]
                    top_left_box_status = top_left_box_value.get_attribute("class")
                    surrounding_box_status_dict[top_left_box_key] = top_left_box_status
                except:
                    continue

                # obtain top box key and status
                top_box_status = ""
                try:
                    top_box_key = "x_" + str(int(current_box_parse[2])-1) + "_" + str(int(current_box_parse[4]))
                    top_box_value = dict_of_box_variables[top_box_key]
                    top_box_status = top_box_value.get_attribute("class")
                    surrounding_box_status_dict[top_box_key] = top_box_status
                except:
                    continue

                # obtain top-right box key and status
                top_right_box_status = ""
                try:
                    top_right_box_key = "x_" + str(int(current_box_parse[2])-1) + "_" + str(int(current_box_parse[4])+1)
                    top_right_box_value = dict_of_box_variables[top_right_box_key]
                    top_right_box_status = top_right_box_value.get_attribute("class")
                    surrounding_box_status_dict[top_right_box_key] = top_right_box_status
                except:
                    continue

                # obtain left box key and status
                left_box_status = ""
                try:
                    left_box_key = "x_" + str(int(current_box_parse[2])) + "_" + str(int(current_box_parse[4])-1)
                    left_box_value = dict_of_box_variables[left_box_key]
                    left_box_status = left_box_value.get_attribute("class")
                    surrounding_box_status_dict[left_box_key] = left_box_status
                except:
                    continue

                # obtain right box key and status
                right_box_status = ""
                try:
                    right_box_key = "x_" + str(int(current_box_parse[2])) + "_" + str(int(current_box_parse[4])+1)
                    right_box_value = dict_of_box_variables[right_box_key]
                    right_box_status = right_box_value.get_attribute("class")
                    surrounding_box_status_dict[right_box_key] = right_box_status
                except:
                    continue

                # obtain bottom-left box key and status
                bottom_left_box_status = ""
                try:
                    bottom_left_box_key = "x_" + str(int(current_box_parse[2])+1) + "_" + str(int(current_box_parse[4])-1)
                    bottom_left_box_value = dict_of_box_variables[bottom_left_box_key]
                    bottom_left_box_status = bottom_left_box_value.get_attribute("class")
                    surrounding_box_status_dict[bottom_left_box_key] = bottom_left_box_status
                except:
                    continue

                # obtain bottom box key and status
                bottom_box_status = ""
                try:
                    bottom_box_key = "x_" + str(int(current_box_parse[2])+1) + "_" + str(int(current_box_parse[4]))
                    bottom_box_value = dict_of_box_variables[bottom_box_key]
                    bottom_box_status = bottom_box_value.get_attribute("class")
                    surrounding_box_status_dict[bottom_box_key] = bottom_box_status
                except:
                    continue

                # obtain bottom-right box key and status
                bottom_right_box_status = ""
                try:
                    bottom_right_box_key = "x_" + str(int(current_box_parse[2])+1) + "_" + str(int(current_box_parse[4])+1)
                    bottom_right_box_value = dict_of_box_variables[bottom_right_box_key]
                    bottom_right_box_status = bottom_right_box_value.get_attribute("class")
                    surrounding_box_status_dict[bottom_right_box_key] = bottom_right_box_status
                except:
                    continue

                print(surrounding_box_status_dict)

                try:
                    # count surrounding box values that == 'square blank'

                    # obtain number of boxes surrounding current box that are open
                    free_neighbors_count = int(current_box_status[-1])

                    if free_neighbors_count == 0:
                        continue
                        # print("Current box open surrounding boxes:", current_box_status_integer)

                    else:
                        try:
                            # build surrounding box status counter dictionary
                            box_status_counter = Counter(surrounding_box_status_dict.values())
                            print("Square Blanks:", box_status_counter["square blank"])
                            print("Box status counter:", box_status_counter)

                            if free_neighbors_count == box_status_counter["square blank"]:
                                print("Free Neighbors match is", True)

                                if top_left_box_status == "square blank":
                                    actionChains.context_click(top_left_box_value).perform()
                                    top_left_box_status = "square bombflagged"

                                if top_box_status == "square blank":
                                    actionChains.context_click(top_box_value).perform()
                                    top_box_status = "square bombflagged"

                                if top_right_box_status == "square blank":
                                    actionChains.context_click(top_right_box_value).perform()
                                    top_right_box_status = "square bombflagged"

                                if left_box_status == "square blank":
                                    actionChains.context_click(left_box_value).perform()
                                    left_box_status = "square bombflagged"

                                if right_box_status == "square blank":
                                    actionChains.context_click(right_box_value).perform()
                                    right_box_status = "square bombflagged"

                                if bottom_left_box_status == "square blank":
                                    actionChains.context_click(bottom_left_box_value).perform()
                                    bottom_left_box_status = "square bombflagged"

                                if bottom_box_status == "square blank":
                                    actionChains.context_click(bottom_box_value).perform()
                                    bottom_box_status = "square bombflagged"

                                if bottom_right_box_status == "square blank":
                                    actionChains.context_click(bottom_right_box_value).perform()
                                    botom_right_box_status = "square bombflagged"

                        except:
                            continue

                except:
                    continue

            else:
                continue


print("Games run:", counter, "(note: counter broken; need to fix; count needs to align with bombdeath count")

# x_1_1 = driver.find_element_by_id("1_1")
# val = x_1_1.get_attribute("class")
# print("This is the x_1_1 class", val)
# x_1_1.click()
# val = x_1_1.get_attribute("class")
# print("This is the x_1_1 class", val)