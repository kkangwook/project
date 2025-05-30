# tunebat: artist-song-key-camelot-bpm-duration-popularity-energy-danceability-happiness-acousticness-instrumentalness-liveness-speechiness-loudness

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

from selenium.webdriver.chrome.options import Options
# 로봇 무시 
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

# 크롬 driver 생성 
driver_path = ChromeDriverManager().install()
correct_driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
driver = webdriver.Chrome(service=Service(executable_path=correct_driver_path), options=options)

# 대상 url 이동 
driver.get('https://tunebat.com/')
time.sleep(7)

########################여기에 질문 삽입#################################
########################################################################
query = ['bts 다이너마이트', '뉴진스 디토','계은숙 기다리는여심','조용필 bounce','비스트 숨','이문세 휘파람']
########################################################################

for i in query:
    # 검색창 
    box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/section/section/main/div/form/div/span/input'))
    )
    box.clear()  # 이전 검색 지우기
    box.send_keys(i) # 검색창에 쿼리넣기
    box.send_keys(Keys.ENTER) #엔터
    
    # 검색 결과의 첫 번째 항목 클릭
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/section/section/main/div/div[2]/div[2]/div[1]/a'))
    )
    if btn:
        btn.click() #클릭
    else:
        continue
    # 데이터 수집
    time.sleep(2)
    data1 = driver.find_elements(By.CLASS_NAME, 'ant-typography') #여러정보들
    lists=[] #데이터 저장될 리스트 생성 
    k=0
    #가수-제목-키-카멜롯-bpm-길이 정보 가져오기 
    prelists=[]
    for item in data1:
        prelists.append(item.text)
        k+=1            #이걸로 enumerate대체 
        if k>21: break
    if prelists[13].startswith('Label'):
        lists.extend([prelists[0],prelists[1],prelists[14],prelists[16],prelists[18],prelists[20]])
    else:
        lists.extend([prelists[0],prelists[1],prelists[13],prelists[15],prelists[17],prelists[19]])
    # popularity-energy-danceability-happiness-acousticness-instrumentalness-liveness-speechiness-loudness
    data2 = driver.find_elements(By.CLASS_NAME, 'ant-progress-text') 
    for item in data2:
        lists.append(item.text)
    #출력 
    print(lists)
    # 홈으로 돌아가기
    home = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/section/section/div[1]/div/div[1]/a'))
    )
    home.click()
    time.sleep(2)  # 홈페이지 로딩을 위한 대기

driver.quit()



#melon: song-artist-genre-lyric-like
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

f=open('./example.csv','w',encoding='utf-8-sig',newline='')
writer=csv.writer(f)
writer.writerow(['song','artist','genre','lyric','like'])

from selenium.webdriver.chrome.options import Options
# 로봇 무시 
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

# 크롬 driver 생성 
driver_path = ChromeDriverManager().install()
correct_driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
driver = webdriver.Chrome(service=Service(executable_path=correct_driver_path), options=options)

#-----------------------------query입력---------------------------------
query = ['bts 다이너마이트', '뉴진스 디토','계은숙 기다리는여심','조용필 bounce','비스트 숨','이문세 휘파람']
#----------------------------------------------------------------------

url='https://www.melon.com/index.htm'
driver.get(url)
time.sleep(3)
data=[]

for i in query:
    try:
        # 홈페이지로 직접 이동
        driver.get(url)
        time.sleep(3)
        
        box=driver.find_element(By.ID,'top_search')
        box.clear()
        box.send_keys(i)
        box.send_keys(Keys.ENTER)
        time.sleep(2)
        div=driver.find_element(By.ID,'frm_songList')
        memo=div.find_element(By.CLASS_NAME,'btn_icon_detail')
        memo.click()
        time.sleep(2)
        info=[]
        song=driver.find_element(By.CLASS_NAME, 'song_name')
        info.append(song.text)
        artist=driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[1]/div[2]/a/span[1]')
        info.append(artist.text)
        genre=driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[2]/dl/dd[3]')
        info.append(genre.text)
        lyric=driver.find_element(By.ID, 'd_video_summary')
        info.append(lyric.text.replace('\n',' '))
        artist_info=driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[1]/div[2]/a/span[1]')
        artist_info.click()
        time.sleep(2)
        like=driver.find_element(By.ID, 'd_like_count')
        info.append(like.text)
        writer.writerow(info)
        print(f"Successfully processed: {i}")  # 진행상황 확인용
        
    except Exception as e:
        print(f"Error with {i}: {str(e)}")  # 에러 발생시 출력
        continue  # 다음 곡으로 진행

print(data)
driver.quit()
f.close()



# song, artist
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

from selenium.webdriver.chrome.options import Options
# 로봇 무시 
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

# 크롬 driver 생성 
driver_path = ChromeDriverManager().install()
correct_driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")
driver = webdriver.Chrome(service=Service(executable_path=correct_driver_path), options=options)

info=[]
url='https://www.melon.com/chart/age/index.htm?chartType=YE&chartGenre=KPOP&chartDate=2024'
driver.get(url)
time.sleep(2)
name1=driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/div[4]/div/div[2]/div[1]/form/table/tbody/tr[1]/td[4]/div/div/div[1]/span/strong/a')
info.append(name1.text)
name2=driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/div[4]/div/div[2]/div[1]/form/table/tbody/tr[1]/td[4]/div/div/div[2]/div[1]/a')
info.append(name2.text)




for i in range(1, 51):
    song=driver.find_element(By.XPATH,f'/html/body/div/div[3]/div/div/div[4]/div/div[2]/div[1]/form/table/tbody/tr[{i}]/td[4]/div/div/div[1]/span/strong/a' )
    artist=driver.find_element(By.XPATH,f'/html/body/div/div[3]/div/div/div[4]/div/div[2]/div[1]/form/table/tbody/tr[{i}]/td[4]/div/div/div[2]/div[1]/a')
    print(song.text, artist.text)
time.sleep(1)
btn=driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div/div[4]/div/div[2]/div[2]/span/a')
btn.click()
time.sleep(1)
for i in range(51, 101):
    song=driver.find_element(By.XPATH,f'/html/body/div/div[3]/div/div/div[4]/div/div[2]/div[1]/form/table/tbody/tr[{i}]/td[4]/div/div/div[1]/span/strong/a' )
    artist=driver.find_element(By.XPATH, f'/html/body/div/div[3]/div/div/div[4]/div/div[2]/div[1]/form/table/tbody/tr[{i}]/td[4]/div/div/div[2]/div[1]/a')
    print(song.text, artist.text)

driver.quit()



