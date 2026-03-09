import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://hdps.cwa.gov.tw/static/state.html"
ACTIVESTATIONS = "stations.json"

def get_active_stations():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    active_stations = {}
    
    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        
        data_rows = driver.find_elements(By.XPATH, "//tr[@class='active']/following-sibling::tr")
        
        for row in data_rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 5:
                st_id = cols[0].text.strip()
                st_name = cols[1].text.strip()
                active_stations[st_id] = st_name
                    
    except Exception as e:
        print(f"擷取失敗: {e}")
    finally:
        driver.quit()
        
    return active_stations

def save_to_json(data, filename=ACTIVESTATIONS):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"觀測站資料已成功備份至 {filename}")
    except Exception as e:
        print(f"存檔失敗: {e}")