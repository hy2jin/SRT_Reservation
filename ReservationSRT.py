import settings
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import subprocess

def openChrome():
    #브라우저 꺼짐 방지 
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # 불필요한 에러 메시지 없애기
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    loginUrl = "https://etk.srail.kr/cmc/01/selectLoginForm.do"
    driver.get(loginUrl)
    driver.implicitly_wait(15)

    print("브라우저 열기 성공")
    return driver

def login(driver, ID, PW):
    wait = WebDriverWait(driver, 30)    # 최대 30초까지 대기
    eleID = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[1]/div[1]/input')))
    eleID.send_keys(ID);print("ID 입력 성공")
    elePW = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[1]/div[2]/input')))
    elePW.send_keys(PW);print("PW 입력 성공")
    loginBtn = driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[1]/div[2]/div/div[2]/input')
    loginBtn.click()
    driver.implicitly_wait(5)
    return driver

def searchTrain(driver, fromName: str, toName: str, targetDate: int, targetTime: int):
    print("SRT 조회 페이지 접속")
    driver.get("https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000")
    driver.implicitly_wait(5)

    eleFrom = driver.find_element(By.ID, "dptRsStnCdNm")
    eleFrom.clear()
    eleFrom.send_keys(fromName)

    eleTo = driver.find_element(By.ID, "arvRsStnCdNm")
    eleTo.clear()
    eleTo.send_keys(toName)

    eleDate = driver.find_element(By.ID, "dptDt")
    Select(eleDate).select_by_value(str(targetDate))

    targetTime = "0" + str(targetTime) if targetTime < 10 else str(targetTime)
    eleTime = driver.find_element(By.ID, "dptTm")
    Select(eleTime).select_by_value(targetTime + "0000")

    print(f"출발역:{fromName}, 도착역:{toName}\n날짜:{targetDate}, 시간:{targetTime}시 이후 SRT 조회중...")

    searchBtn = driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input')
    searchBtn.click()
    driver.implicitly_wait(5)
    time.sleep(1)
    
    return driver


def getTrain(driver, trainStartNum: int, trainCount: int):
    isBook = False      # 예약 됐는지 확인용
    refreshCount = 0    # 새로고침 횟수

    while True:
        for i in range(trainStartNum, trainStartNum + trainCount):
            try:
                seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
            except:
                continue
            if "예약하기" in seat:
                print("예약 가능!!!!!!!!!!!!!!")
                time.sleep(0.5)
                reservationBtn = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7) > a")
                reservationBtn.click()
                isBook = True
                break
        if isBook:
            return refreshCount

        time.sleep(2)
        while True:
            try:
                searchBtn = driver.find_element(By.XPATH, '//*[@id="search_top_tag"]/input')
                break
            except:
                time.sleep(0.5)
                pass
        driver.execute_script("arguments[0].click();", searchBtn)
        refreshCount += 1
        print(f"새로고침 {refreshCount}회")
        driver.implicitly_wait(10)
        time.sleep(2)


driver = openChrome()

ID = settings.SRT_INFO['ID']
PW = settings.SRT_INFO['PW']
driver = login(driver, ID, PW)
print("로그인 성공")
    
FROM    = settings.SRT_INFO['FROM']
TO      = settings.SRT_INFO['TO']
DATE    = settings.SRT_INFO['DATE']
TIME    = settings.SRT_INFO['TIME']
driver = searchTrain(driver, FROM, TO, DATE, TIME)

TRAIN_START_NUM = settings.SRT_INFO['TRAIN_START_NUM']
TRAIN_COUNT = settings.SRT_INFO['TRAIN_COUNT']
refreshCount = getTrain(driver, TRAIN_START_NUM, TRAIN_COUNT)

subprocess.call(['python', 'SendGmail.py', '--count', str(refreshCount)])
# subprocess.call(['python', 'PlayBeep.py'])