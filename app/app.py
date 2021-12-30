import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import seaborn as sns
import os

if os.name == 'posix':
    font_manager.fontManager.addfont('font/NanumGothicCoding-Regular.ttf')
    plt.rc("font", family='NanumGothicCoding')
else:
    plt.rc("font", family="Malgun Gothic")
    


# Sidebar
add_selectbox = st.sidebar.selectbox(
    "과거 지표와 비교하는 코로나19",
    ("선택", "오미크론", "주식", '코로나와 소득수준', '사회적 거리두기')
)

# Data
df = pd.read_csv('./data/trends-extend.csv')
df_covid  = pd.read_csv('./data/covid_data_.csv')

# Body
st.title('How serious is covid now?')

st.header('오늘 코로나19')
st.caption(f'updated: {df.iloc[0, 0]}')
st.subheader('서울')
col1, col2, col3 = st.columns(3)
col1.metric('총 확진자', f'{df.iloc[0, 1]}명', f'{df.iloc[0, 1] - df.iloc[1, 1]}명')
col2.metric('추가 확진자 ', f'{df.iloc[0, 2]}명', f'{df.iloc[0, 2] - df.iloc[1, 2]}명')
col3.metric('사망자', f'{df.iloc[0, 6]}명', f'{df.iloc[0, 6] - df.iloc[1, 6]}명')

st.subheader('전국')
col1, col2, col3 = st.columns(3)
col1.metric('총 확진자', f'{df.iloc[0, 8]}명', f'{df.iloc[0, 8] - df.iloc[1, 8]}명')
col2.metric('추가 확진자 ', f'{df.iloc[0, 9]}명', f'{df.iloc[0, 9] - df.iloc[1, 9]}명')
col3.metric('사망자', f'{df.iloc[0, 12]}명', f'{df.iloc[0, 12] - df.iloc[1, 12]}명')

st.header('데이터')
st.dataframe(df)

# pyarrow.lib.ArrowTypeError: ("Expected bytes, got a 'int' object", 'Conversion failed for column value with type object')
# df_temp = df.astype(str)

df_seoul = df.iloc[:, [0, 6, 1, 3, 4]]
df_seoul.set_index('서울시 기준일', inplace=True)

df_seoul_bar = df.iloc[:, [0, 9]]
df_seoul_bar.loc[:, '서울시 기준일'] = df_seoul_bar['서울시 기준일'].apply(lambda x: x[3:5] + x[6:8])
df_seoul_bar.set_index('서울시 기준일', inplace=True)

df_seoul_line = df.iloc[:, [0, 2, 9]]
df_seoul_line.loc[:, '서울시 기준일'] = df_seoul_line['서울시 기준일'].apply(lambda x: x[3:5] + x[6:8])
df_seoul_line.set_index('서울시 기준일', inplace=True)

st.header('최근 일주일 코로나19')

st.subheader('추가 확진자')
st.bar_chart(df_seoul_bar.iloc[:7])

with st.expander('소스 코드 확인'):
    st.code("""import pandas as pd
import streamlit as st

df = pd.read_csv('./data/trends-extend.csv')

df_seoul = df.iloc[:, [0, 1, 3, 4, 6]]
df_seoul.set_index('서울시 기준일', inplace=True)

df_seoul_bar = df.iloc[:, [0, 2, 8]]
df_seoul_bar.set_index('서울시 기준일', inplace=True)

st.header('최근 일주일 코로나19')
st.subheader('추가 확진자')
st.bar_chart(df_seoul_bar[:7])
    """, language='python')

st.header('한 달 간격으로 보는 코로나19')

st.subheader('총 확진자')
st.area_chart(df_seoul[::30])

st.subheader('추가 확진자')
st.bar_chart(df_seoul_line[::30])

with st.expander('소스 코드 확인'):
    st.code("""import pandas as pd
import streamlit as st
    
df = pd.read_csv('./data/trends-extend.csv')
    
df_seoul = df.iloc[:, [0, 1, 3, 4, 6]]
df_seoul.set_index('서울시 기준일', inplace=True)
    
df_seoul_bar = df.iloc[:, [0, 2, 5]]
df_seoul_bar.set_index('서울시 기준일', inplace=True)
    
st.header('한 달 간격으로 보는 코로나19')
 st.line_chart(df_seoul[::30])
st.bar_chart(df_seoul_bar[::30])
    """, language='python')


st.subheader("기간별 확진자 증가추이")
x= df_covid["확진일"].value_counts().sort_index()

fig , ax = plt.subplots(figsize =  (20,10))

sns.lineplot( x.index, x.values ,color = "r", ax = ax)
ax.set_title("기간별 확진자 증가 추이")
ax.set_ylabel("확진자수")
st.pyplot(fig)
st.write('20.3.10 ~ 21-12-15 까지의 코로나 확진자수를 나타낸 라인 그래프입니다.20년도에는 집단감염원인이 그래프의 변동성을 키웠고 21년도에 들어서면서 집단감염이 아닌 지역감염으로 번짐에 따라 확진자수가 가파르게 증가하는 것을 볼 수 있습니다.')

t = df_covid["접촉력"].value_counts().sort_values().tail(10)

st.subheader("접촉력 파악")
fig ,ax  = plt.subplots(figsize = (10,8))
sns.set_palette("Reds", 10)
sns.barplot(t.index , t.values , ax = ax)
plt.xticks(rotation = 45)
st.pyplot(fig)
st.write('전체 기간 확진자 접촉력에 대해 파악한 막대 그래프입니다.최근 지역감염이 급격하게 증가하며 "기타확진자 접촉", "감염경로조사중" 등 원인을 파악하기 어려운 경우가 다분한것으로 보입니다.')

df_covid["퇴원"] = df_covid["퇴원현황"].str.contains("퇴원", na=False)
df_covid["사망"] = df_covid["퇴원현황"].str.contains("사망", na=False)

퇴원_value = df_covid["퇴원현황"].value_counts()

st.subheader("퇴원자 사망자 비교")

fig , ax  = plt.subplots(figsize = (13,10))

wedgeprops={'width': 0.6, 'edgecolor': 'w', 'linewidth': 5}
colors = ["green","red"]

ax.pie(x = 퇴원_value.values, labels = 퇴원_value.index, autopct='%.1f%%'
      ,  startangle=260, counterclock=False,  wedgeprops=wedgeprops, textprops ={'size' :20}, colors = colors)
st.pyplot(fig)
st.write(' 확진자중 퇴원과 사망한 확진자의 분포를 나타낸 파이차트 입니다. 파이차트만으로는 확진자 중 사망자가 1%로 적은걸 알 수 있습니다. 하지만 이는 잘못된 결론이라고 판단이 듭니다.코로나의 치명률은 연령대에 다르기 때문입니다. 현재 데이터가 부족해 분석을 진행하지는 못하지만 조사해본 봐로는 20대의 경우 치명률이 0.01%이고 30대 0.04%, 40대 0.06%, 50대 0.26%로 1% 미만이지만 코로나 치명률은 고령층으로 갈수록 크게 뜁니다. 60대는 1.05%, 70대는 5.57%, 80대 이상은 18.69%에 달했다.이와 같이 단순 총 사망자 분포를 통해 코로나가 치명적이지 않다고 단정 지을 수는 없다고 생각합니다.')

x  = df_covid["거주지"].value_counts().head(20)

st.subheader("지역별 확진자 수 파악 ")
fig, ax = plt.subplots(figsize = (10,8))
sns.barplot(x.values, x.index  , ax =ax , color = 'r')

ax.set_title("거주지 별 확진자 수 ")
plt.xticks(rotation = 45)
st.pyplot(fig)
st.write('거주지별 확진자수를 나타낸 막대차트입니다. 서울시 거주지 인구수는 송파구, 강서구, 노원구, 관악구 순으로 많습니다. 하지만 코로나 확진자수는 완전히 거주지인구수에 비례하게 나타나지 않는 모습을 볼 수 있습니다. ')
