import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
import streamlit_authenticator as stauth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import numpy as np
@st.experimental_memo
def load_lottie(url:str):
    r = requests.get(url)

    if r.status_code != 200:
        return None
    return r.json()

lottie_url = 'https://assets6.lottiefiles.com/packages/lf20_5edeys7f.json'
lottie_json = load_lottie(lottie_url)

# st_lottie(
#     lottie_json,
#     speed=1,
#     # reverse='Ture',
#     loop=True,
#     quality='low',
#     width=200
#     )

db = firestore.client()

with st.form("my_form",clear_on_submit=False):
    date = st.date_input('date').strftime('%Y-%m-%d')
    time = st.time_input('time',value=datetime.time(17,45)).strftime('%H:%M')
    name = st.text_input('name',value='김규덕')
    age = st.selectbox('age', range(20,65),index=10)
    part = st.text_input('part',value='가공')
    phone = st.text_input('phone',value='010-')
    place = st.selectbox('place', ['고양팩토스타디움','파주시 배드민턴 전용구장'])
    data = { name : {
        '가입일/생성일' : [date, datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')],
        '동호회' : ['배드민턴','탁구'],
        '장소/시간' : [place, time],
        '부서/나이/연락처' : [part,age,phone]
    }}
    checkbox_val = st.checkbox("Double Check")
    if checkbox_val == True:
        submitted = st.form_submit_button('Submit', disabled=True)
    else:
        submitted = st.form_submit_button('Submit')
    if submitted :        
        db.collection('activity').document('배드민턴').update(data)

    db = db.collection('activity').document('배드민턴').get()

# for doc in db.to_dict().keys():
#     st.write(doc)
        # st.write(f"{doc.id} >>> {doc.to_dict()}")

st.write('---')
with st.form('output_form',):
    count = 0
    st.header(f'{date}-{time}')
    st.header(f'{place}')
    st.success('[네이버지도](%s)' % f'https://map.naver.com/v5/directions/-/14114397.866921965,4540303.012815246,%EA%B3%A0%EC%96%91%ED%8C%A9%ED%86%A0%EC%8A%A4%ED%83%80%EB%94%94%EC%9B%80,1966063934,PLACE_POI/-/transit?c=14111433.1227196,4538425.9290852,12.89,0,0,0,dh')

    st.warning('[카카오맵](%s)' % 'https://map.kakao.com/link/to/고양팩토스타디움,37.722334,126.791838')
    submitted = st.form_submit_button('참여')
    if submitted :
        count+=1
    st.info(f"{count}명")
st.write('---')
if st.button('홈으로'):
    switch_page('club')
