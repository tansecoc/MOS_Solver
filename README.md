# MOS_Solver

1. Use a set to create guess set
2. Check face value every click; if facewon, then pause program with input
3. Use get function in dictionary to get key value, but if value does not appear then return default value
4. Create board box value refresh function

Traceback (most recent call last):
  File "/Users/casimerotanseco/PycharmProjects/MOS_Solver/MOS_Solver_Prototype_4.py", line 91, in <module>
    face_element = driver.find_element_by_id("face")
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py", line 360, in find_element_by_id
    return self.find_element(by=By.ID, value=id_)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py", line 976, in find_element
    return self.execute(Command.FIND_ELEMENT, {
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/selenium/webdriver/remote/webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/selenium/webdriver/remote/errorhandler.py", line 241, in check_response
    raise exception_class(message, screen, stacktrace, alert_text)
selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: Please enter your name to submit your score (3)
Message: unexpected alert open: {Alert text : Please enter your name to submit your score (3)}
  (Session info: chrome=88.0.4324.182)


Process finished with exit code 1
