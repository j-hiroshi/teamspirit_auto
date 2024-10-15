from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.date_manager import DateManager
from time import sleep


class BrowserOperation:
    HOME_URL = "https://teamspirit-7491.lightning.force.com/lightning/page/home"

    def __init__(self):
        # 使用しているChromeブラウザのバージョンにあったDriverがインストールされます
        # バージョンに相違がない場合はインストールされません
        chrome_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service)
        self.driver.implicitly_wait(5)

    def pageMove(self, url):
        try:
            self.driver.get(url)
        except Exception:
            raise

    def login(self, username, password):
        username_input = self.driver.find_elements(By.ID, "username")
        username_input[0].send_keys(username)

        password_input = self.driver.find_elements(By.ID, "password")
        password_input[0].send_keys(password)

        username_input[0].submit()
        sleep(3)
        if self.HOME_URL != self.driver.current_url:
            raise Exception

    def work_entry(self, start_time, end_time):
        date_manager = DateManager()
        date_manager.create_business_days()

        shadow_root = self.driver.find_element(
            By.TAG_NAME, "force-aloha-page"
        ).shadow_root
        iframe = shadow_root.find_element(By.CSS_SELECTOR, "iframe")
        self.driver.switch_to.frame(iframe)

        for date in date_manager.business_days:
            # 1日ずつ勤怠入力
            self.driver.find_element(By.ID, "ttvTimeSt" + date).click()
            sleep(0.3)

            # 開始/終了入力
            self.driver.find_element(By.ID, "startTime").send_keys(start_time)
            self.driver.find_element(By.ID, "endTime").send_keys(end_time)

            self.driver.find_element(By.ID, "dlgInpTimeOk").click()
            sleep(3)

            # 工数入力
            self.driver.find_element(By.ID, "dailyWorkCell" + date).click()
            sleep(1)
            self.driver.find_element(By.ID, "empWorkOk").click()
            sleep(3)

    def session_clear(self):
        self.driver.quit()
