import os
import sys
import time
import json
import selenium.webdriver.remote.webelement
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

global driver

def get_element(field: str, label: str, by: By, classname: str):
    temp = list(filter(lambda elem: elem.get_attribute(field) == label, driver.find_elements(by, classname)))
    if len(temp) == 0:
        print("Error: couldn't find button!")
        return None
    else:
        return temp[0]
def handle_playlist(playlist):
    driver.get(playlist["url"])
    time.sleep(1)
    more_button = get_element("data-testid","more-button",By.TAG_NAME,"Button")
    more_button.click()
    time.sleep(0.2)
    edit_button = driver.find_elements(By.CLASS_NAME, "wC9sIed7pfp47wZbmU6m")[2]
    edit_button.click()
    name_input = get_element("data-testid", "playlist-edit-details-name-input",By.TAG_NAME,"input")
    name_input.send_keys(playlist["name"])
    if playlist.get("description") != None:
        description_input = get_element("data-testid", "playlist-edit-details-description-input", By.TAG_NAME, "input")
        description_input.send_keys(playlist["description"])
    save_button = get_element("data-testid", "playlist-edit-details-save-button", By.TAG_NAME,"button")
    save_button.click()
    time.sleep(0.5)

def init_driver():
    options = Options()
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    options.add_argument("user-data-dir=" + os.getcwd() + "/User Data")
    driver = webdriver.Chrome(options=options)
    driver.get("https://open.spotify.com/")
    return driver


if __name__ == '__main__':
    file = open("playlists.json", "r")
    data = json.load(file)
    playlists = data["playlists"]
    file.close()
    driver = init_driver()
    for elem in playlists:
        handle_playlist(elem)
    driver.close()
