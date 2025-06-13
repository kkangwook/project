# 데이터 불러오기
df=pd.read_csv('./final_chart_out_in.csv',encoding='utf-8-sig')

#결측치 확인후 제거
df.isnull().sum()
df.dropna(axis='index',how='any',inplace=True)

# 거의 1대1로 클래스간 불균형은 없음
np.unique(df['target'],return_counts=True) #[0,1]: [324,290]

#이상치 확인(like는 이상치가 있어도 유의미한 값이라 생각해 유지)
df.max(), df.min() # bpm은 50~204, 나머지 수치형데이터는 0~100사이로 정상범위
np.unique(df['camelot']) #camelot 범주형 데이터는 모두 카멜롯 범위안

# like컬럼의 콤마제거 후 숫치화
def comma_remover(x):
    return int(x.replace(',',''))
df['like']=df['like'].apply(comma_remover)  # like는 14에서 725898사이

# 장르는 여러개 존재하는 경우도 있어서 앞의 대표 장르로 통일
import re
def one_genre(x):
    a=re.compile(r'[,].*') #콤마+모든문자 기준
    return re.sub(a,'',x) #콤마포함 콤마이후로 나오는 모든 문자 제거하고 앞의 장르만 남김
df['genre']=df['genre'].apply(one_genre)

# 개수가 적은 장르는 기타장르로 변경
np.unique(df['genre'],return_counts=True) #일렉트로니카, 키즈등의 장르는 수가 너무 작음
df.loc[~df['genre'].isin(['랩/힙합', '발라드', '록/메탈', '댄스', 'R&B/Soul', '인디음악', '성인가요/트로트',
       '포크/블루스']),'genre']='기타' # isin에 들어가지 않은 장르는 기타로



# 사인-코사인 인코딩-> 숫자는 각도의 x,y 2차원으로, AB조성은 0 or 1로 -> 23차원대신 3차원으로
def camelot_sin(x):
    angle = 2 * np.pi * (x - 1) / 12  # 12개 키를 0~2π의 각도로 매핑(0:0도, 1π:180도, 2π:360도)
    return np.sin(angle) # 해당 각도의 y좌표 (사인값) 계산.

def camelot_cos(x):
    angle = 2 * np.pi * (x - 1) / 12
    return np.cos(angle) # 해당 각도의 x좌표 (코사인값) 계산.

def number(x):
    return int(x[:-1])  #숫자만 가져오기

# apply함수 두번사용하여 숫자만 가져와 사인-코사인 인코딩 함수 적용
df['camelot_sin']=np.round(df['camelot'].apply(number).apply(camelot_sin),2)
df['camelot_cos']=np.round(df['camelot'].apply(number).apply(camelot_cos),2)

# A는 0으로, B는 1로
def get_str(x):
    return 0 if x[-1]=='A' else 1
df['camelot_AB']=df['camelot'].apply(get_str)

# 장르는 원핫인코딩
df=pd.get_dummies(df,columns=['genre'],drop_first=True,dtype='int') #9개의 장르를 8차원으로

# 불필요한 컬럼 제거하고 target컬럼을 맨뒤로
df.drop(columns=['camelot','year'],inplace=True)
df = df[ [col for col in df.columns if col != 'target']+['target'] ]

# x,y로 나누고 test세트 분리
x=df.iloc[:,1:-1]; y=df.iloc[:,-1]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=123)







