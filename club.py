import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.header('IMI Critical Engineering Club')

c1, c2, c3 = st.columns([1,1,1])

with c1:
    st.image('https://cdn.pixabay.com/photo/2021/03/02/19/26/snowshoes-6063630_960_720.jpg',use_column_width=True)
    if st.button('배드민턴'):
        switch_page('배드민턴')
    
with c2:
    st.image('https://cdn.pixabay.com/photo/2019/01/21/13/58/table-tenis-3946115_960_720.jpg',use_column_width=True)
    if st.button('탁구'):
        switch_page('탁구')

with c3:
    st.image('https://cdn.pixabay.com/photo/2018/03/08/20/36/ball-3209809_960_720.jpg',use_column_width=True)
    if st.button('풋살'):
        switch_page('풋살')


c4, c5, c6 = st.columns([1,1,1])

with c4:
    st.image('https://cdn.pixabay.com/photo/2015/11/20/08/17/meat-1052571_960_720.jpg',use_column_width=True)
    if st.button('파티'):
        switch_page('파티')

with c5:
    st.image('https://cdn.pixabay.com/photo/2016/04/23/20/21/smart-1348189_960_720.jpg',use_column_width=True)
    if st.button('카풀'):
        switch_page('카풀')

