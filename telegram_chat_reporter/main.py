import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import PIL
import time

def find_on_screen(screenshot: str):
    """
    :param screenshot: path to screenshot
    :return: coordinates of the located region
    Finds the screenshot on the screen
    """
    CONFIDENCE = 0.9
    xpath = f'static/{screenshot}'
    width, height = PIL.Image.open(xpath).size
    region = None
    while region is None:
        region = pyautogui.locateOnScreen(xpath, grayscale=True, confidence=CONFIDENCE)
    return region, width, height


def click_on_region(screenshot: str, offset: tuple = None):
    """
    :param screenshot: path to screenshot
    :param offset: relative mouse coordinates offset
    :return:
    Moves mouse to center of found region and clicks
    """
    if not offset:
        region, width, height = find_on_screen(screenshot)
        pyautogui.moveTo(region.left + width//2, region.top + height//2)
        pyautogui.click()
    else:
        region, width, height = find_on_screen(screenshot)
        pyautogui.moveTo(region.left + width//2 + offset[0], region.top + height//2 + offset[1])
        pyautogui.click()


# Class for webdriver
class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_position(400, 100)

    def connect(self, link):
        self.driver.get(link)


# Program entry to open Telegram chats and locate regions using images
def main():
    # Chats to get reported
    CHATS = ['boris_rozhin', 'grey_zone', 'go338', 'omonmoscow', 'wingsofwar', 'chvkmedia', 'hackberegini', 'mig41',
         'pezdicide', 'SergeyKolyasnikov', 'MedvedevVesti', 'SIL0VIKI', 'balkanossiper', 'pl_syrenka',
         'brussinf', 'lady_north', 'sex_drugs_kahlo', 'usaperiodical', 'russ_orientalist', 'vladlentatarsky',
         'neoficialniybezsonov', 'rybar', 'milinfolive']
    domain = 'https://www.t.me/'

    # btn class for selenium to wait untill button appears and is clickable
    btn_cls = '.tgme_action_button_new'
    for chat in CHATS:
        driver = Driver()
        link = domain + chat
        try:
            driver.connect(link)
            wait = WebDriverWait(driver.driver, 10)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, btn_cls))).click()
            click_on_region('open_in_telegram.png')
        except:
            print("[ERROR]::Channel does not exist")
            continue
        time.sleep(5)
        click_on_region('burger.png')
        driver.driver.close()
        click_on_region('report.png')
        click_on_region('violence.png')
        time.sleep(1)
        pyautogui.moveRel((500, 0))
        pyautogui.click()
        click_on_region('report_btn.png')
        click_on_region('additional_details.png', (20, 20))
        pyautogui.typewrite("Spreading war in Ukraine. Spreading propaganda and disinformation.")
        time.sleep(0.4)
        click_on_region('report_btn1.png')
        
if __name__=='__main__':
    main()
