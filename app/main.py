import streamlit as st
import pandas as pd
import numpy as np

# Sideba.r
add_selectbox = st.sidebar.selectbox(
    "과거 지표와 비교하는 코로나19",
    ("선택", "오미크론", "주식", '코로나와 소득수준', '사회적 거리두기')
)

# Data
df = pd.read_csv('/app/data/trends-extend.csv')

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

df_seoul = df.iloc[:, [0, 1, 3, 4, 6]]
df_seoul.set_index('서울시 기준일', inplace=True)

df_seoul_bar = df.iloc[:, [0, 2, 5]]
df_seoul_bar.set_index('서울시 기준일', inplace=True)

st.header('한 달 간격으로 보는 코로나19')

st.subheader('총 확진자')
st.line_chart(df_seoul[::30])

st.subheader('추가 확진자')
st.bar_chart(df_seoul_bar[::30])

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

st.header('전체 코로나19')

st.subheader('총 확진자')
st.line_chart(df_seoul)

st.subheader('추가 확진자')
st.bar_chart(df_seoul_bar)

with st.expander('소스 코드 확인'):
    st.code("""import pandas as pd
import streamlit as st

df = pd.read_csv('~/data/trends-extend.csv')

df_seoul = df.iloc[:, [0, 1, 3, 4, 6]]
df_seoul.set_index('서울시 기준일', inplace=True)

df_seoul_bar = df.iloc[:, [0, 2, 5]]
df_seoul_bar.set_index('서울시 기준일', inplace=True)
    
st.header('전체 코로나19')

st.subheader('총 확진자')
st.line_chart(df_seoul)

st.subheader('추가 확진자')
st.bar_chart(df_seoul_bar)
    """, language='python')
