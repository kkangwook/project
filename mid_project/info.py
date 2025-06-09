# 한국 음원 audio_feature사이트: TuneBat
 데이터 출처
Spotify Web API 활용
사이트는 70 M+ 곡의 키, BPM 등의 메타데이터를 Spotify에서 가져옵니다.
Tunebat 자체 분석 외에 이 Spotify 데이터베이스를 기반으로 한 정보도 포함 

Essentia.js 기반 브라우저 분석
파일 업로드 시 브라우저 내에서 Essentia.js(스페인 바르셀로나 UPF의 Music Technology Group(MTG) 개발)를 사용해 분석합니다 
Energy, danceability, happiness 등 ML 기반 추정 지표는 학습된 분석 모델로 계산됩니다 

✅ 신뢰성 평가
키(BPM, Camelot key)
Spotify API에서 가져오며, Tunebat 내 분석과 비교해 제공됨.
Spotify 메타데이터는 정확도가 그리 높지 않다는 지적도 존재(< 33% 정확도) 
반면 Tunebat의 브라우저 분석도 “다른 상용 키/BPM 분석보다 더 나은 경우도 있다”고 공식 언급 

Sentiment (energy/danceability/happiness)
모두 ML 모델로 추정된 값이며, 절대적 진실이라기보다는 ‘곡 특성의 상대적 분석 결과’로 이해하는 것이 좋습니다 

커뮤니티·전문가 의견
Reddit / MP3Tag 등에서 Tunebat은 "유용하다"지만, 정확도 최상급이라기보다 참고용으로 사용됨 

🧭 정리
출처: Spotify API + Essentia.js + 자체 ML 모델 기반 분석.
BPM/키: 비교적 믿을 만하지만, Spotify 기본 메타는 부정확할 수 있음 (특히 키 정보).
표정값 (energy 등): 지표적 참고용이며, 절대값이 아님.
결론: “정확한 사이트”라기보다는 믿을 만한 참고 사이트입니다.



# 모델 정확도 높히기
-svm도 사용해보기
-cos-sin encoding말고 ohe도 해보기
-3년단위로 해보기
-장르 숫자세서 일정개수 미만인 애들은 전부 기타로 치환하고 모델만을어보기
-가중치 달리해서 해보기
-3.5:6.5의 클래스개수 불균형있음
scale_pos_weight = n_negative / n_positive = 850 / 450 ≈ 1.89
XGBClassifier(..., scale_pos_weight=1.89)-> 차트인 예측을 더 민감하게 만들 수 있음


# 카멜롯, 키 중 카멜롯 사용하는게 좋을듯(좀더 사람이 듣는 분위기랑 더 비슷)
 # 카멜롯 인코딩방법: Embedding 또는 Sine/Cosine 인코딩 (권장)
원형 데이터를 숫자로 인코딩할 때는 sin/cos 변환이 최적
-> 시간, 요일, 방향등의 순환 데이터에 사용
-> 원형데이터를 각도로 바꾸고 그 사인/코사인 값을 2차원 벡터로 추가하는것
angle = 2π × (값 - 1) / 12
np.sin(angle)
np.cos(angle)
추후 feature_importance에서 importance_camelot = importance_sin + importance_cos 처럼 합산하기도 함 



--검증으로 roc_auc_score()사용-> 실무에서 더 선호


import numpy as np

camelot_number = 8   # 1~12
angle = 2 * np.pi * (camelot_number - 1) / 12
camelot_sin = np.sin(angle)
camelot_cos = np.cos(angle)

결과:
camelot_sin ≈ 0.866
camelot_cos ≈ -0.5
➡️ 최종 피쳐 벡터: [camelot_sin, camelot_cos, camelot_mode] (3차원)

장점:

1A와 12A가 가깝다는 걸 수학적으로 표현 가능

원형 구조를 유지한 채 숫자 인코딩 가능

많은 실제 모델에서 사용되는 방식 (시간, 각도 등에서)



-------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import csv
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

# 로봇 무시 및 광고 차단 설정
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-notifications')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-infobars')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 크롬 driver 생성 
driver_path = ChromeDriverManager().install()
correct_driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
driver = webdriver.Chrome(service=Service(executable_path=correct_driver_path), options=options)
driver.maximize_window()  # 창 최대화

########################여기에 질문 삽입#################################
year=2024
query = list_2024
########################################################################

f=open(f'./tunebat_{year}.csv','w',encoding='utf-8-sig',newline='')
writer=csv.writer(f)
title_row = ['artist','song','key','camelot','bpm','duration','popularity','energy','danceability','happiness','acousticness','instrumentalness','liveness','speechiness','loudness','year']
writer.writerow(title_row)

def click_element_safely(element, driver):
    """요소를 안전하게 클릭하는 함수"""
    try:
        # 일반적인 클릭 시도
        element.click()
    except ElementClickInterceptedException:
        try:
            # JavaScript로 클릭 시도
            driver.execute_script("arguments[0].click();", element)
        except:
            try:
                # Action chains로 클릭 시도
                ActionChains(driver).move_to_element(element).click().perform()
            except:
                return False
    return True

# 대상 url 이동 
driver.get('https://tunebat.com/')
time.sleep(7)

for i in query:
    try:
        # 검색창 
        box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section/section/main/div/form/div/span/input'))
        )
        box.clear()  # 이전 검색 지우기
        box.send_keys(i) # 검색창에 쿼리넣기
        box.send_keys(Keys.ENTER) #엔터
        
        # 검색 결과의 첫 번째 항목 대기 및 클릭
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/section/section/main/div/div[2]/div[2]/div[1]/a'))
        )
        
        # iframe 제거 시도
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                driver.execute_script("arguments[0].remove();", iframe)
        except:
            pass
        
        # 안전한 클릭 시도
        if not click_element_safely(btn, driver):
            print(f"Failed to click for query: {i}")
            # Write NaN values for failed click
            nan_row = ['NaN'] * (len(title_row) - 1) + [year]
            writer.writerow(nan_row)
            continue
            
        # 데이터 수집
        time.sleep(3)  # 로딩 대기 시간 증가
        
        data1 = driver.find_elements(By.CLASS_NAME, 'ant-typography')
        lists = []
        k = 0
        prelists = []
        for item in data1:
            prelists.append(item.text)
            k += 1
            if k > 21: break
            print(k,item.text)
            
        if prelists[13].startswith('Label'):
            lists.extend([prelists[0],prelists[1],prelists[2],prelists[4],prelists[6],prelists[8]])
        else:
            lists.extend([prelists[0],prelists[1],prelists[2],prelists[4],prelists[6],prelists[8]])
            
        data2 = driver.find_elements(By.CLASS_NAME, 'ant-progress-text')
        for item in data2:
            lists.append(item.text)
            
        lists.append(year)
        print(lists)
        print(prelists)
        
        # Ensure the list has the correct number of elements
        if len(lists) < len(title_row):
            lists.extend(['NaN'] * (len(title_row) - len(lists)))
        writer.writerow(lists)
        
        # 홈으로 돌아가기
        home = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/section/section/div[1]/div/div[1]/a'))
        )
        click_element_safely(home, driver)
        time.sleep(3)  # 홈페이지 로딩을 위한 대기 시간 증가
        
    except Exception as e:
        print(f"Error processing {i}: {str(e)}")
        # Write NaN values for all columns except year when an error occurs
        nan_row = ['NaN'] * (len(title_row) - 1) + [year]
        writer.writerow(nan_row)
        # 에러 발생시 홈으로 돌아가기 시도
        try:
            driver.get('https://tunebat.com/')
            time.sleep(5)
        except:
            pass
        continue

driver.quit()
f.close()
