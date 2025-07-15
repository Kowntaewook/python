from selenium import webdriver
import time
import re

def get_chrome_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(options=options)
    return driver

def brute_force_text_extract(driver, url, label=""):
    driver.get(url)
    time.sleep(5)

    body_text = driver.find_element("tag name", "body").text
    candidates = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', body_text)

    print(f"📦 [{label}] 숫자 후보:", candidates)

    for val in candidates:
        try:
            fval = float(val.replace(",", ""))
            if 800 < fval < 4000:  # KOSPI/KOSDAQ 지수 대략 범위
                return val
        except:
            continue

    return None

if __name__ == "__main__":
    driver = get_chrome_driver(headless=False)

    kospi_url = "https://finance.naver.com/sise/sise_index.nhn?code=KOSPI"
    kosdaq_url = "https://finance.naver.com/sise/sise_index.nhn?code=KOSDAQ"

    kospi = brute_force_text_extract(driver, kospi_url, label="KOSPI")
    kosdaq = brute_force_text_extract(driver, kosdaq_url, label="KOSDAQ")

    print("\n📈 실시간 지수 결과")
    print(f"KOSPI 현재가: {kospi}")
    print(f"KOSDAQ 현재가: {kosdaq}")

    driver.quit()
