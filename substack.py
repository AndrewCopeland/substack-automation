from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import os

# "https://codingforfun.substack.com/publish?utm_source=menu"

class ElementAction:
    def __init__(self, name, by, by_value, click, send_keys, sleep = 1, next_url = "") -> None:
        self.name = name
        self.by = by
        self.by_value = by_value
        self.click = click
        self.send_keys = send_keys
        self.sleep = sleep
        self.next_url = next_url

    def run(self, driver):
        print("Starting '{}'".format(self.name))
        element = driver.find_element(self.by, self.by_value)

        if self.click:
            element.click()

        if self.send_keys != "" and self.send_keys != None:
            element.send_keys(self.send_keys)

        if self.next_url != None and self.next_url != "":
            time.sleep(self.sleep)
            driver.get(self.next_url)
        print("Ending '{}'".format(self.name))
        time.sleep(self.sleep)

def run(email, password, substack_publish_url, title, sub_title, message):
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    driver.get("https://substack.com/sign-in?redirect=%2F")
    actions = [] 
    # login
    actions.append(ElementAction("click login with password", By.XPATH, "//a[contains(text(),'log in with')]", True, None))
    actions.append(ElementAction("enter email", By.NAME, 'email', True, email))
    actions.append(ElementAction("enter password", By.NAME, 'password', True, password))
    actions.append(ElementAction("click the login button", By.XPATH, "//button[contains(text(),'Log in')]", True, None))

    # go to the desired substack
    actions.append(ElementAction("click on dashboard and navigate to desired substack", By.XPATH, "//a[contains(text(),'Writer Dashboard')]", True, None, 1, substack_publish_url))
    actions.append(ElementAction("click new post", By.XPATH, "//a[contains(text(),'New post')]", True, None))

    # enter the post
    actions.append(ElementAction("enter post title", By.ID, "post-title", True, title))
    actions.append(ElementAction("enter the subtitle", By.CLASS_NAME, "subtitle", True, sub_title))
    actions.append(ElementAction("select menu", By.XPATH, "//div[contains(text(),'More')]", True, None))
    actions.append(ElementAction("select code block", By.XPATH, "//span[contains(text(),'Code block')]", True, None))
    actions.append(ElementAction("enter content of message", By.CLASS_NAME, "ProseMirror", True, message))
    actions.append(ElementAction("click the publish button", By.ID, "publish", True, None, 5))
    # actions.append(ElementAction("click publish with xpath", By.XPATH, "//span[contains(text(),'Publish')]", True, None, 5))
    actions.append(ElementAction("send to everyone", By.XPATH, "//button[contains(text(),'Send to everyone now')]", True, None))

    for a in actions:
        a.run(driver)
        # time.sleep(5)

def main():
    email = os.environ["SUBSTACK_EMAIL"]
    password = os.environ["SUBSTACK_PASSWORD"]
    substack_publish_url = os.environ["SUBSTACK_PUBLISH_URL"]

    title = os.environ["SUBSTACK_TITLE"]
    sub_title = os.environ["SUBSTACK_SUB_TITLE"]
    f = open(os.environ["SUBSTACK_MESSAGE_FILE"], 'r')
    message = f.read()

    run(email, password, substack_publish_url, title, sub_title, message)

# if __name__ == "__main__":
#     main()