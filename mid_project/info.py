--질의응답
# 차트인 여부가 중요한 이유는?  차트인 한번하면 인지도상승+추천리스트에오름, 스트리밍수가 기하급수적으로 증가해 스트리밍 수익도 증가, 
    # 다양한 방송사와 미디어는 스트리밍 사이트 순위를 곡의 인기척도로 참고하며 방송출연이나 행사수도 같이 증가해서 가수와 소속사에 큰 이득  
# 차트인-차트아웃은 1년치 top100을 기준으로 3년치 한거 명시하기+ 차트아웃은 수동으로 노래 리스트 찾음 -> 앞의 패턴분석도 년 단위여서 일관성 위해 년단위로함+ 개월과 같은 경우로 할경우
                                                            12개월치를 뽑는다면 1200갠데 하나씩 수동으로 찾기는 너무 많은 시간이 필요
# 카멜롯이 키와 대응된다는것을 설명(둘다 24가지 종류가 1대1 대응)
# 장르 label encoding도 해봤지만 one-hot-encoding이 더 결과 좋았음
# 변수설정한 이유설명하기
    - 키같은 경우 카멜롯과 중복되어서 뺌, 사전조사결과 음원길이는 차트인에 별 영향을 미치지 않아 뻄, happiness와 같은 감정과 관련된 주관적인 특성들도 제거
    - 음악 데이터와 상관없는 liveness(청중여부)같은거 제거 하여 현재의 것만 사용-> 나중에 결과를 보면 알겠지만 xgb의 feature_importance에서 bpm,energy,dan,ac모두 상위권에 위치해 그대로 유지
# 원핫인코딩 한 애들은 상대적으로 feature importance가 낮게 나올수밖에 없음/ 카멜롯의 sin-cos인코딩은 3차원으로 줄였기에 상대적으로 중요도큼
    - feature_importance가 크다-> 손실감소에 큰 기여를 했다-> 
  따라서 a라는 특성이 너무 중요해서 초반에 크게 그 특성으로 나누고 나머지를 세세하게 나눌떄 다른 특성들을 많이써서 a의 feature importance값이 작게 나올수도있어? -> 없다
# shap도 표시 -> 하나의 변수에 대해 그 값이 이진분류에 있어서 음의 영향(클래스0으로)을 줄지 양의 영향(클래스1로예츠되게끔)을 줄지 보여주는 지표
    



#ligthgbm이나 histgradientboosting써보기
#시각화 상관관계도 보기
# 록메탈컬럼*10하거나, 클래스별로 가중치를 달리주거나, 샘플별 록메탈포함한애들 가중치 더 높게주거나 
#xgboostparameter
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')


#앙상블에서는 레이블인코딩도방법,모든변수넣고 feature_importance로 중요도봐서 어떤변수뺄지결정
# class1과 class0의 샘플수 거의 1대1로 샘플불균형의 문제는 없다
# permutation importance로 입력변수 중 하나의 영향을 제거하여 성능의 차이가 얼마나 나는지 확인
# 단순 가수와 음악의 정보만으로 예측가능할까?
# 날씨별 배달음식 추천모델에서 svm vs randomforest특징 가져오기
#차트인예측모델==인기예측모델
# 튠뱃쓴이유-> 스포티파이api지원중단
# chart_out 락/메탈빼보기
# 마지막에 어떤 특징일수록 차트인할수있는지 조건쓰기


#데이터전처리:
1. 결측치 확인후 제거
2. 이상치확인 (min, max)
3. like는 콤마제거후 숫자화
4. 장르는 여러 장르일경우 앞의 대표 장르만 가져옴
5. 
4.카멜롯의 원핫인코딩 vs cos-sin인코딩 + svc vs xgboostclassifier -> auc점수로 확인
5. xgboost와 cos-sin인코딩 선택 후 lightGBM, histgradient boosting과 도 비교-> xgboost
6. xgboost의 feature importance봐서 중요 변수 선택
7. 앙상블에서는 레이블인코딩도방법,모든변수넣고 feature_importance로 중요도봐서 어떤변수뺄지결정 -> 레이블 인코딩보다 원핫인코딩이 나음

# .score는 얼마나 잘 맞추는지, .auc는 예측확률이 얼마나 정확한지(0.51, 0.49이런건 별로-> 덜 맞추더라도 0.8, 0.2이런식으로 나오게끔)

# Define parameter grid to sample from
param_dist = {
    'n_estimators': [50, 100, 200, 300, 500],
    'max_depth': [3, 4, 5, 6, 7, 8],
    'learning_rate': np.linspace(0.01, 0.3, 30),
    'subsample': np.linspace(0.5, 1.0, 6),
    'colsample_bytree': np.linspace(0.5, 1.0, 6),
    'gamma': [0, 0.1, 0.2, 0.3, 0.4],
    'reg_alpha': [0, 0.01, 0.1, 1, 10],  # L1 regularization
    'reg_lambda': [1, 1.5, 2, 3, 5]      # L2 regularization
}

# Setup RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_dist,
    n_iter=50,  # number of random parameter sets to try
    scoring='roc_auc',
    cv=5,
    verbose=1,
    random_state=42,
    n_jobs=-1
)




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
