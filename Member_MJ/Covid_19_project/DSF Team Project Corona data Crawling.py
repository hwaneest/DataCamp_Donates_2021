#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import warnings
warnings.filterwarnings(action='ignore')

from pandas.io.json import json_normalize
import requests # 크롤링을 위함
import json # json파일을 다루기위함
import time # 크롤링에 딜레이를 두기 위함
from tqdm import trange #  크롤링 진행시 progress Bar 


# ### 크롤링 사이트 주소

# https://www.seoul.go.kr/coronaV/coronaStatus.do 발생동향|서울시 코로나 19 

# ### 크롤링 함수 생성 

# In[2]:


# 발생동향|서울시 코로나 19 사이트에서 확진자 상세현황에 있는 데이터를 크콜링 하기 위해서는 두개의 함수 생성이 필요
# URL 정의가 다르기 때문에 각각에 맞는 URL를 넣어서 함수 생성 

# 과거 200000 확진자까지의 데이터를 크롤링하는 함수 

def get_seoul_covid19_past(page_num):
    
    start_no = (page_num - 3) * 100
    
    url = f"https://news.seoul.go.kr/api/27/getCorona19Status/get_status_ajax_pre.php?draw={page_num}"
    url = f"{url}&order%5B0%5D%5Bdir%5D=desc&start={start_no}&length=100"
        
    response = requests.get(url)
    data_json = response.json()
    
    return data_json


# In[5]:


page_list1 = []
all_page = 1
end_page = 2001

for page_no in trange(all_page ,end_page):
    
    # 차단막는 코드, 랜덤으로 time.sleep 지정
    seed = np.random.randint(100)
    np.random.seed(seed)
    a = np.random.randint(3)
    time.sleep(a)
        
        
    df = get_seoul_covid19_past(page_no)
    #json 타입 데이터에서 'data' key와 매칭하는 value 데이터를 데이터프레임으로 변환
    
    df = pd.DataFrame(df["data"]) 
    page_list1.append(df)


# In[80]:


# 크롤링한 결과를 한번에 결합시킬 수 있지만 데이터가 문제없이 크롤링 되었는지 살펴보기위해 따로 저장 
df = pd.concat(page_list1)
df.tail(3)


# In[8]:


#  컬럼명 변경 
df = df.rename(columns = {0 : "연번", 1:"환자" ,2:"확진일", 3:"거주지", 4:"여행력", 5:"접촉력",6:"퇴원현황"})
df.tail(3)


# In[9]:


# 200001~ 현재 확진자까지의 데이터를 크롤링하는 함수

def get_seoul_covid19_today(page_num):
    
    start_num = (page_num - 3) * 100
    
    url = f"https://news.seoul.go.kr/api/27/getCorona19Status/get_status_ajax.php?draw={page_num}"
    url = f"{url}&order%5B0%5D%5Bdir%5D=desc&start={start_num}&length=100"
        
    response = requests.get(url)
    data_json = response.json()
    
    return data_json


# In[10]:


page_list2 = []

#크롤링할 페이지 설정
all_page = 1
end_page = 34

for page_num in trange(all_page ,end_page):
    
    # 차단막는 코드, 랜덤으로 time.sleep 지정
    seed = np.random.randint(100)
    np.random.seed(seed)
    a = np.random.randint(3)
    time.sleep(a)
            
    df = get_seoul_covid19_today(page_num)
    
    #json 타입 데이터에서 'data' key와 매칭하는 value 데이터를 데이터프레임으로 변환
    df = pd.DataFrame(df["data"]) 
    page_list2.append(df)


# In[81]:


df1 =pd.concat(page_list2)
df1.head(3)


# In[16]:


#  컬럼명 변경 
df1 = df1.rename(columns = {0 : "연번", 1:"환자" ,2:"확진일", 3:"거주지", 4:"여행력", 5:"접촉력",6:"퇴원현황"})
df1.tail(3)


# In[82]:


df = pd.concat([df1,df])
df


# In[83]:


df= df.rename(columns = {0 : "연번", 1:"환자" ,2:"확진일", 3:"거주지", 4:"여행력", 5:"접촉력",6:"퇴원현황"})
df


# In[30]:


# csv파일로 저장 
df.to_csv("covid_now.csv")


# ### Preprocessing

# In[84]:


df = pd.read_csv("covid_now.csv", index_col = 0)
df.tail(3)


# In[89]:


#정규표현식 사용을 위해 import re 
import re


# In[90]:


def extract_number(num_string):
    if type(num_string) == str:
        num_string = num_string.replace("corona19", "") # 'corona19'를 제거한 후에 
        num = re.sub("[^0-9]", "", num_string)# 숫자가 아닌 문자 모두 제거 ,re.sub（정규 표현식, 대상 문자열 , 치환 문자）
        # [^0-9] not을 표현하며 0~9를 제외한 문자를 의미 
        
        num = int(num)
        return num
    else:
        return num_string

df["연번"] = df["연번"].map(extract_number)
df    


# In[91]:


def extract_hangeul(origin_text):
    subtract_text = re.sub("[^가-힣]", "", origin_text) # 한글이 아닌 문자 제거
    # [^가-힣] not을 표현하며 가~힣 를 제외한 문자를 의미 
    
    return subtract_text

df["퇴원현황"] = df["퇴원현황"].map(extract_hangeul)
df.loc[df["퇴원현황"].isin(['']), "퇴원현황"] = np.nan # 퇴원현황 값이 없으면 NaN으로 표기 
df


# In[92]:


df["확진일"] = pd.to_datetime(df["확진일"])
df["확진일"] = pd.to_datetime(df["확진일"])
df["년"] = df["확진일"].dt.year
df["월"] = df["확진일"].dt.month
df["일"] = df["확진일"].dt.day
df["주"] = df["확진일"].dt.week


# In[93]:


df.tail(3)


# 20.3.22 ~ 20.4.7 (강화된 거리두기 )  2단계  
# 20.04.08 ~ 20.4,19 (첫 집합금지 명령) 2단계  
# 20.4.20 ~ 20.5.5 (일부조치 완하) 1단계  
# 20.5.6 ~ 20.8.15  (생활속 거리두기) 0단계  
# 20.8.16 ~ 20.8.20 2단계   
# 20.8.21 ~ 20.9.12 2.5 단계   
# 20.9.13 ~ 20.10.10 2단계  
# 20.10.11 ~ 11.16 1단계  
# 20.11.17 ~ 20.11.23 1.5 단계  
# 20.11.24 ~ 20.12.7 2단계  
# 20.12.8 ~ 21.2.14 2.5단계  
# 21.2.15 ~ 21.10.31 2단계   
# 21.11.1 ~ 21.12.17 0단계   
# 21.12.18 ~21.12.19 4단계

# In[94]:


df.loc[df["확진일"].isin(pd.date_range("2020-03-10","2020-03-11")), "거리두기" ] = 0
df.loc[df["확진일"].isin(pd.date_range("2020-03-12","2020-03-21")), "거리두기" ] = 0
df.loc[df["확진일"].isin(pd.date_range("2020-03-22","2020-04-19")), "거리두기" ] = 2
df.loc[df["확진일"].isin(pd.date_range("2020-04-20","2020-05-05")), "거리두기" ] = 1 
df.loc[df["확진일"].isin(pd.date_range("2020-05-06","2020-08-15")), "거리두기" ] = 0
df.loc[df["확진일"].isin(pd.date_range("2020-08-16","2020-08-20")), "거리두기" ] = 2 
df.loc[df["확진일"].isin(pd.date_range("2020-08-21","2020-09-12")), "거리두기" ] = 2.5 
df.loc[df["확진일"].isin(pd.date_range("2020-09-13","2020-10-10")), "거리두기" ] = 2 
df.loc[df["확진일"].isin(pd.date_range("2020-10-11","2020-11-16")), "거리두기" ] = 1 
df.loc[df["확진일"].isin(pd.date_range("2020-11-17","2020-11-23")), "거리두기" ] = 1.5
df.loc[df["확진일"].isin(pd.date_range("2020-11-24","2020-12-07")), "거리두기" ] = 2 
df.loc[df["확진일"].isin(pd.date_range("2020-12-08","2021-02-14")), "거리두기" ] = 2.5 
df.loc[df["확진일"].isin(pd.date_range("2021-02-15","2021-10-31")), "거리두기" ] = 2 
df.loc[df["확진일"].isin(pd.date_range("2021-11-01","2021-12-17")), "거리두기" ] = 0
df.loc[df["확진일"].isin(pd.date_range("2021-12-18","2021-12-19")), "거리두기" ] = 4


# In[95]:


df15 =df.loc[df["확진일"].isin(pd.date_range("2020-03-10","2020-03-11"))]
df1 = df.loc[df["확진일"].isin(pd.date_range("2020-03-12","2020-03-21"))]
df2 = df.loc[df["확진일"].isin(pd.date_range("2020-03-22","2020-04-19"))]
df3 = df.loc[df["확진일"].isin(pd.date_range("2020-04-20","2020-05-05"))]
df4 = df.loc[df["확진일"].isin(pd.date_range("2020-05-06","2020-08-15"))]
df5 = df.loc[df["확진일"].isin(pd.date_range("2020-08-16","2020-08-20"))]
df6 = df.loc[df["확진일"].isin(pd.date_range("2020-08-21","2020-09-12"))]
df7 = df.loc[df["확진일"].isin(pd.date_range("2020-09-13","2020-10-10"))]
df8 = df.loc[df["확진일"].isin(pd.date_range("2020-10-11","2020-11-16"))]
df9 = df.loc[df["확진일"].isin(pd.date_range("2020-11-17","2020-11-23"))]
df10 = df.loc[df["확진일"].isin(pd.date_range("2020-11-24","2020-12-07"))]
df11 = df.loc[df["확진일"].isin(pd.date_range("2020-12-08","2021-02-14"))]
df12 = df.loc[df["확진일"].isin(pd.date_range("2021-02-15","2021-10-31"))]
df13 = df.loc[df["확진일"].isin(pd.date_range("2021-11-01","2021-12-17"))]
df14 = df.loc[df["확진일"].isin(pd.date_range("2021-12-18","2021-12-19"))]


# In[96]:


df = pd.concat([df15, df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14])
df.head(30)


# In[50]:


df.to_csv("covid_data.csv")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




