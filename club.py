#     u'stringExample': u'Hello, World!',
#     u'booleanExample': True,
#     u'numberExample': 3.14159265,
#     u'dateExample': datetime.datetime.now(tz=datetime.timezone.utc),
#     u'arrayExample': [5, True, u'hello'],
#     u'nullExample': None,
#     u'objectExample': {
#         u'a': 5,
#         u'b': True
#     }
# }

# C

# res = collection.document('배드민턴').get().to_dict()

# # R
# res = collection.get() # returns a list

# for i in res:
#     st.write(i.to_dict())

# # U
# res = collection.document('A01').update({
#     'State': 'Chennai',
#     'age': 21
# })

# # D
# res = collection.document('A01').delete() 

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

st.set_page_config(
    page_title="😎",
)

if not firebase_admin._apps:
    cred = credentials.Certificate('club-ecd9c-firebase-adminsdk-4xmc7-a36179a49c.json')
    app = firebase_admin.initialize_app(cred)


# st.session_state.clear()
empty = st.empty()

if 'nickname' not in st.session_state:
    nickname = st.text_input('닉네임 입력(추후 회원기능 도입)')
    st.session_state.nickname = nickname
    
else:
    nickname = empty.text_input('닉네임 입력(추후 회원기능 도입)',value=st.session_state.nickname)
    st.session_state.nickname = nickname

nickname = st.session_state.nickname

st.write(f"Hi, {nickname}🎈")
db = firestore.client()

@st.experimental_singleton
def img(img):
    img = st.image(img,use_column_width=True)
    return img

# @st.experimental_singleton
def expander(title):
    return st.expander(title, expanded=True)

if nickname:
    empty.empty()
    st.header('IMI Critical Engineering Club')
    with expander('dynamic'):
        c = st.columns(3)
        with c[0]:
            img('https://cdn.pixabay.com/photo/2021/03/02/19/26/snowshoes-6063630_960_720.jpg')
            if st.button('배드민턴'):
                switch_page('배드민턴')
            
        with c[1]:
            img('https://cdn.pixabay.com/photo/2019/01/21/13/58/table-tenis-3946115_960_720.jpg')
            if st.button('탁구'):
                switch_page('탁구')

        with c[2]:
            img('https://cdn.pixabay.com/photo/2018/03/08/20/36/ball-3209809_960_720.jpg')
            if st.button('축구'):
                switch_page('축구')

    with expander('static'):
        c = st.columns(3)

        with c[0]:
            img('https://cdn.pixabay.com/photo/2015/11/20/08/17/meat-1052571_960_720.jpg')
            if st.button('파티'):
                switch_page('파티')

        with c[1]:
            img('https://cdn.pixabay.com/photo/2016/04/23/20/21/smart-1348189_960_720.jpg')
            if st.button('카풀'):
                switch_page('카풀')

    logout = st.button('로그아웃')
    if logout:
        st.session_state.clear()
        st.experimental_rerun()
        # switch_page('club')
