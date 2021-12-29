from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import numpy as np
import datetime as dt

PATH = os.getenv('PWD')
url = f'http://openapi.seoul.go.kr:8088/{os.environ["API_TOKEN"]}/xml/TbCorona19CountStatus/1/1/'
r = requests.get(url)
s = BeautifulSoup(r.text, 'lxml')
df = pd.read_csv(PATH + '/data/trends-extend.csv')

latest = df['서울시 기준일'][0]
new = s.s_dt.get_text()
delta = dt.datetime.strptime(new, '%Y.%m.%d.%H') - dt.datetime.strptime(latest, '%y.%m.%d')
date_diff = delta.days

if date_diff == 0:
    exit(0)
elif date_diff == 1:
    pass
else:
    url = f'http://openapi.seoul.go.kr:8088/694a786b456272613832484564666b/xml/TbCorona19CountStatus/1/{date_diff}/'
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'lxml')


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

s_dts = list(map(lambda x: x[2:10], s_dts))
t_dts = list(map(lambda x: x[2:10], t_dts))
lst = list(np.array(ls).T)
new = pd.DataFrame(lst, columns=df.columns)
new = new.append(df, ignore_index=True)
new.to_csv(PATH + '/data/trends-extend.csv', index=False)
