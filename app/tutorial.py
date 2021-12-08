import streamlit as st
import pandas as pd
import numpy as np

'''
It is a tutorial
'''

# SubHeader
st.subheader('subheader')

# Text
st.write('Write something')

# Button
if st.button('click button'):
    st.write('Data Loading..')

# checkbox
if checkbox_btn := st.checkbox('Checkbox Button'):
    st.write('Great!')

# Radio Button
selected_item = st.radio('Radio Part', ('A', 'B', 'C'))

if selected_item == 'A':
    st.write('A!!')
elif selected_item == 'B':
    st.write('B!')
elif selected_item == 'C':
    st.write('C!')

# select box
option = st.selectbox('Please selct in selectbox!', ('apple', 'banana', 'pineapple'))

st.write('You selected:', option)

# multi-select box
multi_select = st.multiselect('Please select somethings in multi selectbox!', ['A', 'B', 'C', 'D'])
st.write('You selected:', multi_select)

# slider
values = st.slider('Select a range of values', 0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

st.write('st.dataframe api')
df = pd.DataFrame(np.random.randn(5, 2), columns=['col %d ' % i for i in range(2)])
st.dataframe(df.style.highlight_max(axis=0))

st.write('st.table api')
st.line_chart(df)