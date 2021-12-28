from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import numpy as np
import datetime as dt

PATH = os.getenv('PWD')
url = 'http://openapi.seoul.go.kr:8088/'+ os.environ['API_TOKEN'] + '/xml/TbCorona19CountStatus/1/1/'
r = requests.get(url)
s = BeautifulSoup(r.text, 'lxml')
df = pd.read_csv(PATH + '/data/trends-extend.csv')
assert str(df.iloc[0]['서울시 기준일']) != str(dt.datetime.strptime(s.s_dt.get_text(), '%Y.%m.%d.%H')), 'Already Udpated'


# Last date를 저장해서 비교하는 방법 사용 가능

def find_and_get(st):
    l = []
    for f in s.find_all(st):
        l.append(f.get_text())
    return l


s_dts = find_and_get('s_dt')
s_hjs = find_and_get('s_hj')
sn_hjs = find_and_get('sn_hj')
s_cares = find_and_get('s_care')
s_recovers = find_and_get('s_recover')
sn_recovers = find_and_get('sn_recover')
s_deaths = find_and_get('s_death')
t_dts = find_and_get('t_dt')
t_hjs = find_and_get('t_hj')
n_hjs = find_and_get('n_hj')
ty_care = find_and_get('ty_care')
recovers = find_and_get('recover')
deaths = find_and_get('death')
ls = [s_dts, s_hjs, sn_hjs, s_cares, s_recovers, sn_recovers, s_deaths, t_dts, t_hjs, n_hjs, ty_care, recovers, deaths]

s_dts = list(map(lambda x: dt.datetime.strptime(x, '%Y.%m.%d.%H'), s_dts))
t_dts = list(map(lambda x: dt.datetime.strptime(x, '%Y.%m.%d.%H'), t_dts))
lst = list(np.array(ls).T)
new = pd.DataFrame(lst, columns=df.columns)
new = new.append(df, ignore_index=True)
new['서울시 기준일'] = new['서울시 기준일'].apply(lambda x: x[2:10] if len(x) == 13 else x)
new['전국 기준일'] = new['전국 기준일'].apply(lambda x: x[2:10] if len(x) == 13 else x)
new.to_csv(PATH + '/data/trends-extend.csv', index=False)
