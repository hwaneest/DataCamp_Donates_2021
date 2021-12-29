import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

# Sidebar
add_selectbox = st.sidebar.selectbox(
    "과거 지표와 비교하는 코로나19",
    ("선택", "오미크론", "주식", '코로나와 소득수준', '사회적 거리두기')
)

# Data
df = pd.read_csv('./data/trends-extend.csv')

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

# st.header('전체 코로나19')
#
# st.subheader('총 확진자')
# st.line_chart(df_seoul)
#
# st.subheader('추가 확진자')
# st.bar_chart(df_seoul_bar)
#
# with st.expander('소스 코드 확인'):
#     st.code("""import pandas as pd
# import streamlit as st
#
# df = pd.read_csv('~/data/trends-extend.csv')
#
# df_seoul = df.iloc[:, [0, 1, 3, 4, 6]]
# df_seoul.set_index('서울시 기준일', inplace=True)
#
# df_seoul_bar = df.iloc[:, [0, 2, 5]]
# df_seoul_bar.set_index('서울시 기준일', inplace=True)
#
# st.header('전체 코로나19')
#
# st.subheader('총 확진자')
# st.line_chart(df_seoul)
#
# st.subheader('추가 확진자')
# st.bar_chart(df_seoul_bar)
#     """, language='python')
#
# # 한글폰트 사용
# if os.name == 'posix':
#     plt.rc("font", family="AppleGothic")
# else:
#     plt.rc("font", family="Malgun Gothic")
#
# df = pd.read_csv('./data/data.csv', index_col = 0)
# df.head(3)
#
# df["확진일"] = pd.to_datetime(df["확진일"])
# x= df["확진일"].value_counts().sort_index()
# fig, ax = plt.subplots(figsize =  (20,10))
#
# sns.lineplot( x.index, x.values , ax = ax,color = "r")
# ax.set_title("기간별 확진자 증가 추이")
# ax.set_ylabel("확진자수")
# plt.show()
# #st.pyplot(fig)
#
# t = df["접촉력"].value_counts().sort_values().tail(10)
# # 전체 기준
# fig3, ax = plt.subplots(figsize=(10, 8))
# sns.set_palette("Reds", 10)
# sns.barplot(t.index, t.values, ax=ax)
# plt.xticks(rotation=45)
# st.pyplot(fig3)
#
# df.loc[df["확진일"].isin(pd.date_range("2020-03-10","2020-03-21")), "거리두기" ] = 0
# df.loc[df["확진일"].isin(pd.date_range("2020-03-22","2020-04-19")), "거리두기" ] = 2
# df.loc[df["확진일"].isin(pd.date_range("2020-04-20","2020-05-05")), "거리두기" ] = 1
# df.loc[df["확진일"].isin(pd.date_range("2020-05-06","2020-08-15")), "거리두기" ] = 0
# df.loc[df["확진일"].isin(pd.date_range("2020-08-16","2020-08-20")), "거리두기" ] = 2
# df.loc[df["확진일"].isin(pd.date_range("2020-08-21","2020-09-12")), "거리두기" ] = 2.5
# df.loc[df["확진일"].isin(pd.date_range("2020-09-13","2020-10-10")), "거리두기" ] = 2
# df.loc[df["확진일"].isin(pd.date_range("2020-10-11","2020-11-16")), "거리두기" ] = 1
# df.loc[df["확진일"].isin(pd.date_range("2020-11-17","2020-11-23")), "거리두기" ] = 1.5
# df.loc[df["확진일"].isin(pd.date_range("2020-11-24","2020-12-07")), "거리두기" ] = 2
# df.loc[df["확진일"].isin(pd.date_range("2020-12-08","2021-02-14")), "거리두기" ] = 2.5
# df.loc[df["확진일"].isin(pd.date_range("2021-02-15","2021-10-31")), "거리두기" ] = 2
# df.loc[df["확진일"].isin(pd.date_range("2021-11-01","2021-12-15")), "거리두기" ] = 0
#
# df13 = df.loc[df["확진일"].isin(pd.date_range("2020-03-10","2020-03-21"))]
# df1 = df.loc[df["확진일"].isin(pd.date_range("2020-03-22","2020-04-19"))]
# df2 = df.loc[df["확진일"].isin(pd.date_range("2020-04-20","2020-05-05"))]
# df3 = df.loc[df["확진일"].isin(pd.date_range("2020-05-06","2020-08-15"))]
# df4 = df.loc[df["확진일"].isin(pd.date_range("2020-08-16","2020-08-20"))]
# df5 = df.loc[df["확진일"].isin(pd.date_range("2020-08-21","2020-09-12"))]
# df6 = df.loc[df["확진일"].isin(pd.date_range("2020-09-13","2020-10-10"))]
# df7 = df.loc[df["확진일"].isin(pd.date_range("2020-10-11","2020-11-16"))]
# df8 = df.loc[df["확진일"].isin(pd.date_range("2020-11-17","2020-11-23"))]
# df9 = df.loc[df["확진일"].isin(pd.date_range("2020-11-24","2020-12-07"))]
# df10 = df.loc[df["확진일"].isin(pd.date_range("2020-12-08","2021-02-14"))]
# df11 = df.loc[df["확진일"].isin(pd.date_range("2021-02-15","2021-10-31"))]
# df12 = df.loc[df["확진일"].isin(pd.date_range("2021-11-01","2021-12-15"))]
#
# df_거리두기 = pd.concat([df13, df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12])
# df_거리두기 = df.set_index("확진일")
# x= df_거리두기.index.value_counts().sort_index()
#
# fig2 ,(ax0,ax1 ) = plt.subplots(2,1 ,figsize =  (20,10), sharey =False) # x,y축값을 동일시
#
# sns.lineplot( x.index, x.values , ax = ax0,color = "r")
# sns.lineplot( df_거리두기.index, df_거리두기["거리두기"] , ax = ax1,color = "r")
#
# ax0.set_title("기간별 확진자수 ")
# ax0.set_ylabel("확진자수")
#
# ax1.set_title("기간별 거리두기 단계 ")
# ax1.set_ylabel("거리두기 단계 ")
#
# fig2.tight_layout() # 메소드는 서브 플롯간에 올바른 간격을 자동으로 유지합니다.
# plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, wspace=0.7, hspace=0.5) #  #subplot 간 간격 조절
# st.pyplot(fig2)
